#!/usr/bin/env python3
"""Fetch provider model lists from env-configured providers and enrich with models.dev.

Usage:
  source ~/.envrc
  python3 ~/ai/skills/model-selection/scripts/fetch_provider_models.py

Output:
  ~/ai/skills/model-selection/provider-models.yaml
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_ENVRC_PATH = Path.home() / ".envrc"
DEFAULT_OUTPUT_PATH = Path.home() / "ai/skills/model-selection/provider-models.yaml"
MODELS_DEV_URL = "https://models.dev/api.json"


def run_curl(
    url: str, headers: Dict[str, str] | None = None, timeout_s: int = 45
) -> Dict[str, Any]:
    cmd = ["curl", "-sS", url]
    if headers:
        for k, v in headers.items():
            cmd.extend(["-H", f"{k}: {v}"])

    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s)
    if proc.returncode != 0:
        raise RuntimeError(
            proc.stderr.strip() or f"curl failed with code {proc.returncode}"
        )

    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        snippet = proc.stdout[:300].replace("\n", " ")
        raise RuntimeError(f"non-JSON response: {snippet}") from exc


def parse_envrc(path: Path) -> Dict[str, str]:
    env: Dict[str, str] = {}
    if not path.exists():
        return env
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line.startswith("export "):
            continue
        body = line[len("export ") :]
        if "=" not in body:
            continue
        k, v = body.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def build_models_dev_index() -> Dict[str, Dict[str, Any]]:
    data = run_curl(MODELS_DEV_URL)
    index: Dict[str, Dict[str, Any]] = {}
    for provider_id, provider_obj in data.items():
        models = provider_obj.get("models", {})
        for model_id, model_obj in models.items():
            index[model_id] = {
                "provider": provider_id,
                "id": model_obj.get("id", model_id),
                "name": model_obj.get("name"),
                "family": model_obj.get("family"),
                "context": (model_obj.get("limit") or {}).get("context"),
                "output": (model_obj.get("limit") or {}).get("output"),
                "modalities": model_obj.get("modalities"),
                "open_weights": model_obj.get("open_weights"),
            }
    return index


def models_dev_lookup(model_id: str, idx: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    candidates = [model_id]
    if model_id.endswith(":free"):
        candidates.append(model_id[: -len(":free")])
    if ":" in model_id:
        candidates.append(model_id.split(":", 1)[0])

    seen = set()
    for c in candidates:
        if c in seen:
            continue
        seen.add(c)
        hit = idx.get(c)
        if hit:
            out = dict(hit)
            out["matched"] = True
            return out

    return {"matched": False}


def normalize_model_items(
    provider: str, payload: Dict[str, Any]
) -> List[Dict[str, Any]]:
    items = payload.get("data") if isinstance(payload, dict) else None

    if provider == "replicate" and items is None and isinstance(payload, dict):
        items = payload.get("results")

    if provider == "ollama" and items is None and isinstance(payload, dict):
        items = payload.get("models")

    if not isinstance(items, list):
        return []

    out: List[Dict[str, Any]] = []
    for m in items:
        if not isinstance(m, dict):
            continue
        mid = m.get("id") or m.get("name")
        if provider == "ollama":
            mid = m.get("model") or m.get("name")
        if not mid:
            owner = m.get("owner")
            name = m.get("name")
            if owner and name:
                mid = f"{owner}/{name}"
        if not mid:
            continue
        out.append(
            {
                "id": str(mid),
                "name": m.get("name"),
                "context_length": m.get("context_length") or m.get("context_window"),
            }
        )
    return out


def fetch_provider_models(
    env: Dict[str, str], ollama_base_url: str
) -> Dict[str, Dict[str, Any]]:
    known = {
        "openrouter": bool(env.get("OPENROUTER_API_KEY")),
        "groq": bool(env.get("GROQ_API_KEY")),
        "mistral": bool(env.get("MISTRAL_API_KEY")),
        "nvidia": bool(env.get("NVIDIA_API_KEY")),
        "replicate": bool(env.get("REPLICATE_API_TOKEN")),
        "cloudflare": bool(
            env.get("CLOUDFLARE_API_KEY") and env.get("CLOUDFLARE_ACCOUNT_ID")
        ),
        "ollama": bool(env.get("OLLAMA_API_KEY")),
        "tavily": bool(env.get("TAVILY_API_KEY")),
    }

    results: Dict[str, Dict[str, Any]] = {}

    for provider, enabled in known.items():
        if not enabled:
            continue

        try:
            if provider == "openrouter":
                payload = run_curl(
                    "https://openrouter.ai/api/v1/models",
                    headers={
                        "Authorization": f"Bearer {env['OPENROUTER_API_KEY']}",
                        "HTTP-Referer": "https://localhost",
                        "X-Title": "model-selection-inventory",
                    },
                )
                models = [
                    m
                    for m in normalize_model_items(provider, payload)
                    if m["id"].endswith(":free") or "/free" in m["id"]
                ]
                results[provider] = {
                    "status": "ok",
                    "endpoint": "https://openrouter.ai/api/v1/models",
                    "free_only": True,
                    "models": models,
                }

            elif provider == "groq":
                payload = run_curl(
                    "https://api.groq.com/openai/v1/models",
                    headers={"Authorization": f"Bearer {env['GROQ_API_KEY']}"},
                )
                results[provider] = {
                    "status": "ok",
                    "endpoint": "https://api.groq.com/openai/v1/models",
                    "models": normalize_model_items(provider, payload),
                }

            elif provider == "mistral":
                payload = run_curl(
                    "https://api.mistral.ai/v1/models",
                    headers={"Authorization": f"Bearer {env['MISTRAL_API_KEY']}"},
                )
                results[provider] = {
                    "status": "ok",
                    "endpoint": "https://api.mistral.ai/v1/models",
                    "models": normalize_model_items(provider, payload),
                }

            elif provider == "nvidia":
                payload = run_curl(
                    "https://integrate.api.nvidia.com/v1/models",
                    headers={"Authorization": f"Bearer {env['NVIDIA_API_KEY']}"},
                )
                results[provider] = {
                    "status": "ok",
                    "endpoint": "https://integrate.api.nvidia.com/v1/models",
                    "models": normalize_model_items(provider, payload),
                }

            elif provider == "replicate":
                payload = run_curl(
                    "https://api.replicate.com/v1/models",
                    headers={"Authorization": f"Token {env['REPLICATE_API_TOKEN']}"},
                )
                results[provider] = {
                    "status": "ok",
                    "endpoint": "https://api.replicate.com/v1/models",
                    "models": normalize_model_items(provider, payload),
                }

            elif provider == "cloudflare":
                account = env["CLOUDFLARE_ACCOUNT_ID"]
                payload = run_curl(
                    f"https://api.cloudflare.com/client/v4/accounts/{account}/ai/models/search",
                    headers={
                        "Authorization": f"Bearer {env['CLOUDFLARE_API_KEY']}",
                        "Content-Type": "application/json",
                    },
                )
                models = payload.get("result", []) if isinstance(payload, dict) else []
                normalized = []
                for m in models:
                    if isinstance(m, dict) and m.get("name"):
                        normalized.append(
                            {
                                "id": m.get("name"),
                                "name": m.get("name"),
                                "context_length": None,
                            }
                        )
                results[provider] = {
                    "status": "ok",
                    "endpoint": f"https://api.cloudflare.com/client/v4/accounts/{account}/ai/models/search",
                    "models": normalized,
                }

            elif provider == "ollama":
                # Prefer local daemon inventory of installed models.
                endpoint = f"{ollama_base_url.rstrip('/')}/api/tags"
                payload = run_curl(endpoint)
                results[provider] = {
                    "status": "ok",
                    "endpoint": endpoint,
                    "models": normalize_model_items(provider, payload),
                }

            elif provider == "tavily":
                results[provider] = {
                    "status": "unsupported",
                    "reason": "No standard public model-list endpoint tied to this env key.",
                    "models": [],
                }

        except Exception as exc:  # noqa: BLE001
            results[provider] = {
                "status": "error",
                "error": str(exc),
                "models": [],
            }

    return results


def yaml_quote(value: Any) -> str:
    s = "" if value is None else str(value)
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


def write_yaml(path: Path, payload: Dict[str, Any]) -> None:
    lines: List[str] = []
    lines.append(f"generated_at: {yaml_quote(payload['generated_at'])}")
    lines.append("sources:")
    for src in payload["sources"]:
        lines.append(f"  - {yaml_quote(src)}")
    lines.append("providers:")

    for provider, info in sorted(payload["providers"].items()):
        lines.append(f"  {provider}:")
        lines.append(f"    status: {yaml_quote(info.get('status'))}")
        if "endpoint" in info:
            lines.append(f"    endpoint: {yaml_quote(info.get('endpoint'))}")
        if "free_only" in info:
            lines.append(f"    free_only: {str(bool(info.get('free_only'))).lower()}")
        if "reason" in info:
            lines.append(f"    reason: {yaml_quote(info.get('reason'))}")
        if "error" in info:
            lines.append(f"    error: {yaml_quote(info.get('error'))}")

        models = info.get("models", [])
        lines.append(f"    model_count: {len(models)}")
        lines.append("    models:")
        for m in models:
            md = m.get("models_dev", {"matched": False})
            lines.append(f"      - id: {yaml_quote(m.get('id'))}")
            lines.append(f"        name: {yaml_quote(m.get('name'))}")
            if m.get("context_length") is not None:
                lines.append(f"        context_length: {m.get('context_length')}")
            lines.append(
                f"        models_dev_matched: {str(bool(md.get('matched'))).lower()}"
            )
            if md.get("matched"):
                lines.append(f"        models_dev_id: {yaml_quote(md.get('id'))}")
                lines.append(
                    f"        models_dev_provider: {yaml_quote(md.get('provider'))}"
                )
                lines.append(f"        models_dev_name: {yaml_quote(md.get('name'))}")
                lines.append(
                    f"        models_dev_family: {yaml_quote(md.get('family'))}"
                )
                if md.get("context") is not None:
                    lines.append(f"        models_dev_context: {md.get('context')}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch model lists for providers discovered in an env file, "
            "restrict OpenRouter to free models, enrich with models.dev, "
            "and write a provider-grouped YAML inventory."
        )
    )
    parser.add_argument(
        "--envrc",
        default=str(DEFAULT_ENVRC_PATH),
        help=f"Env file with provider keys (default: {DEFAULT_ENVRC_PATH})",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help=f"Output YAML file path (default: {DEFAULT_OUTPUT_PATH})",
    )
    parser.add_argument(
        "--ollama-base-url",
        default="http://localhost:11434",
        help="Base URL for Ollama model listing (default: http://localhost:11434)",
    )
    args = parser.parse_args()

    envrc_path = Path(args.envrc).expanduser()
    output_path = Path(args.output).expanduser()

    env = parse_envrc(envrc_path)
    models_dev_idx = build_models_dev_index()
    providers = fetch_provider_models(env, args.ollama_base_url)

    for info in providers.values():
        models = info.get("models", [])
        for m in models:
            m["models_dev"] = models_dev_lookup(m.get("id", ""), models_dev_idx)

    out = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "sources": [str(envrc_path), MODELS_DEV_URL],
        "providers": providers,
    }
    write_yaml(output_path, out)
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
