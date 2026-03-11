from __future__ import annotations

import asyncio
import json
import os
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Annotated

import httpx
import typer
from pydantic import BaseModel, ConfigDict, Field
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="OpenRouter model discovery and testing tool")
console = Console()

MODELS_DEV_URL = "https://models.dev/api.json"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"


class ModelMetadata(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str
    tier: str | None = None
    tool_call: bool = False
    cost: dict | None = None

    @property
    def is_free(self) -> bool:
        # Check explicit tier first
        if self.tier == "free":
            return True
        # Then check ID suffix (common for free models)
        if self.id.endswith(":free"):
            return True
        # Finally check cost if available (0 input and 0 output)
        if self.cost and self.cost.get("input") == 0 and self.cost.get("output") == 0:
            return True
        return False


async def fetch_models_dev() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(MODELS_DEV_URL)
        response.raise_for_status()
        return response.json()


def get_openrouter_key() -> str:
    key = os.getenv("OPENROUTER_API_KEY")
    assert key, "OPENROUTER_API_KEY environment variable is not set"
    return key


async def probe_model(model_id: str, check_tools: bool = False) -> tuple[bool, str]:
    key = get_openrouter_key()
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 5,
    }

    if check_tools:
        payload["messages"] = [{"role": "user", "content": "Find files containing auth"}]
        payload["tools"] = [
            {
                "type": "function",
                "function": {
                    "name": "search_files",
                    "parameters": {
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                    },
                },
            }
        ]

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                OPENROUTER_API_URL, headers=headers, json=payload, timeout=30.0
            )
            if response.status_code != 200:
                return False, f"HTTP {response.status_code}: {response.text}"

            data = response.json()
            if "error" in data:
                return False, data["error"].get("message", "Unknown error")

            if check_tools:
                choices = data.get("choices", [])
                if choices and choices[0].get("message", {}).get("tool_calls"):
                    return True, "SUPPORTS_TOOLS"
                return False, "NO_TOOL_SUPPORT"

            return True, "UP"
        except Exception as e:
            return False, str(e)


@app.command(name="list")
def list_models(
    tools_only: bool = typer.Option(False, "--tools", help="Only show models with tool support"),
    provider: str = "openrouter",
):
    """List free models from models.dev with filters."""

    async def _run():
        data = await fetch_models_dev()
        provider_data = data.get(provider, {}).get("models", {})

        table = Table(title=f"Free {provider.capitalize()} Models")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Tools", style="yellow")

        for model_id, meta_raw in provider_data.items():
            meta = ModelMetadata(**meta_raw)
            if not meta.is_free:
                continue
            if tools_only and not meta.tool_call:
                continue

            table.add_row(
                model_id,
                meta.name,
                "✅" if meta.tool_call else "❌",
            )

        console.print(table)

    asyncio.run(_run())


@app.command()
def probe(
    model_id: str,
    check_tools: bool = typer.Option(False, "--tools", help="Check for tool support"),
):
    """Probe a specific free model."""

    async def _run():
        data = await fetch_models_dev()
        # Ensure it's a free model before probing
        all_models = data.get("openrouter", {}).get("models", {})
        if model_id in all_models:
            meta = ModelMetadata(**all_models[model_id])
            assert meta.is_free, f"Model {model_id} is not free"

        success, message = await probe_model(model_id, check_tools=check_tools)
        if success:
            console.print(f"[green]✅ {model_id}: {message}[/green]")
        else:
            console.print(f"[red]❌ {model_id}: {message}[/red]")

    asyncio.run(_run())


@app.command()
def discover(
    tools_only: bool = typer.Option(True, "--tools", help="Only show models with tool support"),
    provider: str = "openrouter",
):
    """List and probe free models."""

    async def _run():
        data = await fetch_models_dev()
        provider_data = data.get(provider, {}).get("models", {})

        models_to_probe = []
        for model_id, meta_raw in provider_data.items():
            meta = ModelMetadata(**meta_raw)
            if not meta.is_free:
                continue
            if tools_only and not meta.tool_call:
                continue
            models_to_probe.append((model_id, meta))

        console.print(f"Found {len(models_to_probe)} free models to probe...")

        for model_id, meta in models_to_probe:
            success, message = await probe_model(model_id, check_tools=tools_only)
            if success:
                console.print(f"[green]✅ {model_id}: {message}[/green]")
            else:
                console.print(f"[red]❌ {model_id}: {message}[/red]")

    asyncio.run(_run())


@app.command()
def report(
    output: Path = typer.Option(
        Path("openrouter-free-results.md"), help="Output file for the report"
    ),
    provider: str = "openrouter",
):
    """Run discovery and generate a Markdown report for free models."""

    async def _run():
        data = await fetch_models_dev()
        provider_data = data.get(provider, {}).get("models", {})

        models_to_probe = []
        for model_id, meta_raw in provider_data.items():
            meta = ModelMetadata(**meta_raw)
            if not meta.is_free:
                continue
            models_to_probe.append((model_id, meta))

        console.print(f"Generating report for {len(models_to_probe)} free models...")

        results = []
        for model_id, meta in models_to_probe:
            success, message = await probe_model(model_id, check_tools=meta.tool_call)
            results.append(
                {
                    "id": model_id,
                    "name": meta.name,
                    "status": "✅ WORKING" if success else f"❌ {message}",
                    "tools": meta.tool_call,
                }
            )
            status_color = "green" if success else "red"
            console.print(f"[{status_color}]{model_id}: {message}[/{status_color}]")

        # Write markdown
        with open(output, "w") as f:
            f.write(f"# OpenRouter Free Models Test Results\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("| Model | Status | Tools |\n")
            f.write("|-------|--------|-------|\n")
            for r in results:
                tools_icon = "✅" if r["tools"] else "❌"
                f.write(f"| {r['id']} | {r['status']} | {tools_icon} |\n")

        console.print(f"\n[bold green]Report saved to {output}[/bold green]")

    asyncio.run(_run())


if __name__ == "__main__":
    app()
