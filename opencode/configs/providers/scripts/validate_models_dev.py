#!/usr/bin/env python3
"""Validate provider model inventories against models.dev."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PROVIDERS_DIR = ROOT / "configs" / "providers"
IGNORED_PROVIDERS = {"cursor-acp", "qwen-code"}


class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def fetch_models_dev_api() -> dict:
    url = "https://models.dev/api.json"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "opencode-provider-validation/1.0"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode())


def load_provider_configs(targets: list[str]) -> dict[str, dict]:
    provider_files = sorted(PROVIDERS_DIR.glob("*.json"))
    providers = {}
    requested = set(targets)
    for provider_file in provider_files:
        provider_name = provider_file.stem
        if requested and provider_name not in requested:
            continue
        with provider_file.open() as handle:
            providers[provider_name] = json.load(handle)
    return providers


def normalize_model_ids(provider_id: str, model_ids: set[str]) -> set[str]:
    if provider_id == "ollama-cloud":
        return {model_id.removesuffix(":cloud") for model_id in model_ids}
    return model_ids


def print_discrepancy_block(
    provider_id: str,
    in_local_not_dev: list[str],
    in_dev_not_local: list[str],
) -> None:
    print(f"\n  {Colors.YELLOW}{Colors.BOLD}DISCREPANCY DETECTED for '{provider_id}':{Colors.RESET}")

    if in_local_not_dev:
        print(
            f"    {Colors.CYAN}Models in config but NOT in models.dev "
            f"({len(in_local_not_dev)}):{Colors.RESET}"
        )
        for model in in_local_not_dev[:5]:
            print(f"      {Colors.CYAN}- {model}{Colors.RESET}")
        if len(in_local_not_dev) > 5:
            print(
                f"      {Colors.CYAN}... and {len(in_local_not_dev) - 5} more"
                f"{Colors.RESET}"
            )

    if in_dev_not_local:
        print(
            f"    {Colors.MAGENTA}Models in models.dev but NOT in config "
            f"({len(in_dev_not_local)}):{Colors.RESET}"
        )
        for model in in_dev_not_local[:5]:
            print(f"      {Colors.MAGENTA}- {model}{Colors.RESET}")
        if len(in_dev_not_local) > 5:
            print(
                f"      {Colors.MAGENTA}... and {len(in_dev_not_local) - 5} more"
                f"{Colors.RESET}"
            )


def validate_provider(
    provider_id: str,
    provider_cfg: dict,
    models_dev: dict,
) -> tuple[bool, bool]:
    whitelist = set((provider_cfg.get("models") or {}).keys())
    blacklist = set(provider_cfg.get("blacklist") or [])
    overlap = sorted(whitelist & blacklist)

    if overlap:
        print(
            f"  {Colors.RED}{Colors.BOLD}ERROR:{Colors.RESET} "
            f"Models appear in both whitelist and blacklist: {overlap}"
        )
        return False, True

    if provider_id in IGNORED_PROVIDERS:
        print(
            f"  {Colors.YELLOW}{Colors.BOLD}SKIPPED:{Colors.RESET} "
            f"'{provider_id}' is not expected in models.dev yet"
        )
        return True, False

    provider_from_models_dev = models_dev.get(provider_id)
    if not provider_from_models_dev:
        print(
            f"  {Colors.YELLOW}{Colors.BOLD}SKIPPED:{Colors.RESET} "
            f"'{provider_id}' not found in models.dev"
        )
        return True, False

    local_models = normalize_model_ids(provider_id, whitelist | blacklist)
    models_dev_models = normalize_model_ids(
        provider_id,
        set((provider_from_models_dev.get("models") or {}).keys()),
    )

    in_local_not_dev = sorted(local_models - models_dev_models)
    in_dev_not_local = sorted(models_dev_models - local_models)
    has_discrepancies = bool(in_local_not_dev or in_dev_not_local)

    if has_discrepancies:
        print_discrepancy_block(provider_id, in_local_not_dev, in_dev_not_local)
        print(
            f"    {Colors.BOLD}Summary:{Colors.RESET} local={len(local_models)} "
            f"models.dev={len(models_dev_models)} "
            f"symmetric_diff={len(in_local_not_dev) + len(in_dev_not_local)}"
        )
        return True, True

    print(
        f"  {Colors.GREEN}OK{Colors.RESET} models.dev={len(models_dev_models)} "
        f"whitelist={len(whitelist)} blacklist={len(blacklist)}"
    )
    return True, False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("providers", nargs="*", help="Provider IDs to validate")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any discrepancy is found",
    )
    args = parser.parse_args()

    providers = load_provider_configs(args.providers)
    if args.providers:
        missing = sorted(set(args.providers) - set(providers))
        if missing:
            print(f"Unknown providers: {', '.join(missing)}", file=sys.stderr)
            return 2

    models_dev = fetch_models_dev_api()

    print(f"{Colors.BOLD}{Colors.BLUE}Validating providers against models.dev{Colors.RESET}")
    print(f"{Colors.BOLD}Total providers to check: {len(providers)}{Colors.RESET}\n")

    discrepancies = 0
    failures = 0

    for provider_id, provider_cfg in providers.items():
        print(f"{Colors.BOLD}{Colors.WHITE}Provider: {provider_id}{Colors.RESET}")
        ok, has_discrepancy = validate_provider(provider_id, provider_cfg, models_dev)
        if not ok:
            failures += 1
        if has_discrepancy:
            discrepancies += 1
        print()

    print(f"{Colors.BOLD}{Colors.BLUE}Validation summary{Colors.RESET}")
    print(f"{Colors.GREEN}Providers checked:{Colors.RESET} {len(providers)}")
    print(f"{Colors.YELLOW}Providers with discrepancies:{Colors.RESET} {discrepancies}")
    print(f"{Colors.RED}Providers with hard errors:{Colors.RESET} {failures}")

    if failures:
        return 1
    if args.strict and discrepancies:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
