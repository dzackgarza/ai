from __future__ import annotations

import asyncio
import os
from datetime import datetime
from pathlib import Path

import httpx
import typer
from pydantic import BaseModel, ConfigDict
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
        # Union of: explicit tier, :free suffix, OR zero cost
        if self.tier == "free":
            return True
        if self.id.endswith(":free"):
            return True
        # Check both key naming conventions (input/prompt, output/completion)
        if self.cost:
            prompt_cost = self.cost.get("input") or self.cost.get("prompt")
            completion_cost = self.cost.get("output") or self.cost.get("completion")
            if prompt_cost == 0 and completion_cost == 0:
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
        payload["messages"] = [
            {"role": "user", "content": "Find files containing auth"}
        ]
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


@app.command()
def ls(
    tool_calling: bool = typer.Option(
        False, "--tool-calling", "-t", help="Only show models with tool-calling support"
    ),
):
    """List available free models."""

    async def _run():
        data = await fetch_models_dev()
        provider_data = data.get("openrouter", {}).get("models", {})

        table = Table(title="Free OpenRouter Models")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Tool Calling", style="yellow")

        for model_id, meta_raw in provider_data.items():
            meta = ModelMetadata(**meta_raw)
            if not meta.is_free:
                continue
            if tool_calling and not meta.tool_call:
                continue

            table.add_row(
                model_id,
                meta.name,
                "✅" if meta.tool_call else "❌",
            )

        console.print(table)

    asyncio.run(_run())


@app.command()
def check(
    model_id: str = typer.Argument(
        None, help="Model ID to probe (probes all if omitted)"
    ),
    tool_calling: bool = typer.Option(
        False,
        "--tool-calling",
        "-t",
        help="When probing all, filter by tool-calling support",
    ),
):
    """Probe availability of free models."""

    async def _run():
        data = await fetch_models_dev()
        provider_data = data.get("openrouter", {}).get("models", {})

        if model_id:
            if model_id not in provider_data:
                console.print(
                    f"[red]Error: Model {model_id} not found in models.dev[/red]"
                )
                return
            meta = ModelMetadata(**provider_data[model_id])
            assert meta.is_free, f"Model {model_id} is not free"
            models_to_probe = [(model_id, meta)]
        else:
            models_to_probe = []
            for m_id, meta_raw in provider_data.items():
                meta = ModelMetadata(**meta_raw)
                if not meta.is_free:
                    continue
                if tool_calling and not meta.tool_call:
                    continue
                models_to_probe.append((m_id, meta))

        console.print(f"Probing {len(models_to_probe)} model(s)...")

        for m_id, meta in models_to_probe:
            success, message = await probe_model(m_id, check_tools=meta.tool_call)
            if success:
                console.print(f"[green]✅ {m_id}: {message}[/green]")
            else:
                console.print(f"[red]❌ {m_id}: {message}[/red]")

    asyncio.run(_run())


@app.command()
def report(
    output: Path = typer.Option(
        Path("OPENROUTER_FREE.md"), help="Output file for the audit report"
    ),
):
    """Audit all free models and generate a Markdown report."""

    async def _run():
        data = await fetch_models_dev()
        provider_data = data.get("openrouter", {}).get("models", {})

        models_to_probe = []
        for model_id, meta_raw in provider_data.items():
            meta = ModelMetadata(**meta_raw)
            if not meta.is_free:
                continue
            models_to_probe.append((model_id, meta))

        console.print(f"Auditing {len(models_to_probe)} free models...")

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

        with open(output, "w") as f:
            f.write("# OpenRouter Free Models Audit\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("| Model | Status | Tool Calling |\n")
            f.write("|-------|--------|--------------|\n")
            for r in results:
                tools_icon = "✅" if r["tools"] else "❌"
                f.write(f"| {r['id']} | {r['status']} | {tools_icon} |\n")

        console.print(f"\n[bold green]Audit report saved to {output}[/bold green]")

    asyncio.run(_run())


if __name__ == "__main__":
    app()
