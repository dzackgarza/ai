#!/usr/bin/env python3
"""Convenience CLI for template-defined llm-runner requests."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Annotated, Any

import typer
from llm_runner import (
    ErrorDetail,
    ErrorResponse,
    RunOverrides,
    RunRequest,
    list_models,
    run_request,
)
from llm_templating_engine import Bindings, TemplateReference, TextFileBinding
from pydantic import BaseModel

CONTEXT_SETTINGS: dict[str, list[str]] = {"help_option_names": ["-h", "--help"]}
app = typer.Typer(
    add_completion=False,
    pretty_exceptions_enable=False,
    context_settings=CONTEXT_SETTINGS,
)

_WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
_PROMPTS_ROOT = (_WORKSPACE_ROOT / "prompts").resolve()


def _write_payload(output_path: str | None, payload: BaseModel) -> None:
    content = payload.model_dump_json(indent=2)
    if output_path is None:
        typer.echo(content)
        return
    Path(output_path).expanduser().write_text(content)


def _write_error(output_path: str | None, error: Exception) -> None:
    _write_payload(
        output_path,
        ErrorResponse(
            error=ErrorDetail(type=type(error).__name__, message=str(error))
        ),
    )


def _split_assignment(raw: str, *, option_name: str) -> tuple[str, str]:
    if "=" not in raw:
        raise ValueError(f"Invalid {option_name} format {raw!r}; expected name=value.")
    key, value = raw.split("=", 1)
    key = key.strip()
    if key == "":
        raise ValueError(f"Invalid {option_name} format {raw!r}; binding name is empty.")
    return key, value.strip()


def _resolve_template_path(raw_path: str) -> Path:
    candidate = Path(raw_path).expanduser()
    if candidate.is_absolute():
        return candidate.resolve()
    cwd_candidate = (Path.cwd() / candidate).resolve()
    if cwd_candidate.exists():
        return cwd_candidate
    return (_PROMPTS_ROOT / candidate).resolve()


def _resolve_file_path(raw_path: str) -> Path:
    return Path(raw_path).expanduser().resolve()


def _build_bindings(
    *,
    file_bindings: list[str] | None,
    variable_bindings: list[str] | None,
    json_bindings: list[str] | None,
    json_file_bindings: list[str] | None,
) -> Bindings:
    data: dict[str, Any] = {}
    text_files: list[TextFileBinding] = []

    for raw in variable_bindings or []:
        key, value = _split_assignment(raw, option_name="--var")
        if key in data:
            raise ValueError(f"Duplicate binding name: {key}")
        data[key] = value

    for raw in json_bindings or []:
        key, value = _split_assignment(raw, option_name="--data")
        if key in data:
            raise ValueError(f"Duplicate binding name: {key}")
        try:
            data[key] = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON for binding {key!r}: {exc}") from exc

    for raw in json_file_bindings or []:
        key, value = _split_assignment(raw, option_name="--data-file")
        if key in data:
            raise ValueError(f"Duplicate binding name: {key}")
        source = _resolve_file_path(value)
        try:
            data[key] = json.loads(source.read_text())
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f"Structured binding file not found: {source}"
            ) from exc
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Invalid JSON in structured binding file {source}: {exc}"
            ) from exc

    file_names = {binding.name for binding in text_files}
    for raw in file_bindings or []:
        key, value = _split_assignment(raw, option_name="--file")
        if key in data or key in file_names:
            raise ValueError(f"Duplicate binding name: {key}")
        text_files.append(TextFileBinding(name=key, path=str(_resolve_file_path(value))))
        file_names.add(key)

    return Bindings(data=data, text_files=text_files)


@app.command()
def run_command(
    ctx: typer.Context,
    template: Annotated[
        str | None,
        typer.Argument(
            help="Template path. Relative paths resolve from the workspace prompts directory.",
        ),
    ] = None,
    list_models_flag: Annotated[
        bool,
        typer.Option(
            "--list-models",
            help="List available llm-runner model slugs and exit.",
        ),
    ] = False,
    provider: Annotated[
        str | None,
        typer.Option(
            "--provider",
            help="Optional provider name used with --list-models.",
        ),
    ] = None,
    file_bindings: Annotated[
        list[str] | None,
        typer.Option(
            "--file",
            "-f",
            help="Expose a text file binding as name=path.",
        ),
    ] = None,
    variable_bindings: Annotated[
        list[str] | None,
        typer.Option(
            "--var",
            "-v",
            help="Expose a string binding as name=value.",
        ),
    ] = None,
    json_bindings: Annotated[
        list[str] | None,
        typer.Option(
            "--data",
            help="Expose a structured binding as name=<json>.",
        ),
    ] = None,
    json_file_bindings: Annotated[
        list[str] | None,
        typer.Option(
            "--data-file",
            help="Expose a structured binding from a JSON file as name=path.",
        ),
    ] = None,
    model: Annotated[
        str | None,
        typer.Option("--model", "-m", help="Override template frontmatter models."),
    ] = None,
    temperature: Annotated[
        float | None,
        typer.Option("--temperature", "-t", help="Override template temperature."),
    ] = None,
    max_tokens: Annotated[
        int | None,
        typer.Option("--max-tokens", help="Override template max_tokens."),
    ] = None,
    retries: Annotated[
        int | None,
        typer.Option("--retries", help="Override template retries."),
    ] = None,
    output_path: Annotated[
        str | None,
        typer.Option("--output", "-o", help="Write response JSON to this file."),
    ] = None,
) -> None:
    """Execute one template-defined llm-runner request."""
    if list_models_flag:
        try:
            for slug in list_models(provider):
                typer.echo(slug)
            return
        except ValueError as exc:
            _write_error(output_path, exc)
            raise typer.Exit(code=1) from exc
    if template is None:
        typer.echo(ctx.get_help())
        raise typer.Exit(code=1)

    try:
        bindings = _build_bindings(
            file_bindings=file_bindings,
            variable_bindings=variable_bindings,
            json_bindings=json_bindings,
            json_file_bindings=json_file_bindings,
        )
        template_path = _resolve_template_path(template)
        response = asyncio.run(
            run_request(
                RunRequest(
                    template=TemplateReference(path=str(template_path)),
                    bindings=bindings,
                    overrides=RunOverrides(
                        models=[model] if model is not None else None,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        retries=retries,
                    ),
                )
            )
        )
        _write_payload(output_path, response)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        _write_error(output_path, exc)
        raise typer.Exit(code=1) from exc


def main() -> None:
    """Run the convenience llm-runner wrapper."""
    app()


if __name__ == "__main__":
    main()
