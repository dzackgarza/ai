#!/usr/bin/env python3

import json
import urllib.request

# ANSI color codes for colorful output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def fetch_models_dev_api():
    """Fetch canonical model data from models.dev API."""
    url = "https://models.dev/api.json"
    req = urllib.request.Request(url, headers={"User-Agent": "opencode-config-builder/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        raise RuntimeError(f"Failed to fetch models.dev API: {e}")

def assert_provider_partition_matches_models_dev(provider_id):
    """Validate provider config against models.dev canonical source."""
    
    # Load provider config
    providers_dir = "/home/dzack/ai/opencode/configs/providers"
    provider_file = f"{providers_dir}/{provider_id}.json"
    
    with open(provider_file, "r") as f:
        provider_cfg = json.load(f)

    whitelist = set((provider_cfg.get("models") or {}).keys())
    blacklist = set(provider_cfg.get("blacklist") or [])
    
    # Check for overlap (hard error - config bug)
    overlap = sorted(whitelist & blacklist)
    if overlap:
        raise RuntimeError(
            f"{Colors.RED}{Colors.BOLD}Error:{Colors.RESET} "
            f"Provider '{provider_id}' has models in both whitelist and blacklist: {overlap}"
        )

    local_models = whitelist | blacklist
    models_dev_models = get_models_dev_provider_models(provider_id)
    
    # Provider not in models.dev - skip validation but warn
    if models_dev_models is None:
        print(
            f"{Colors.YELLOW}{Colors.BOLD}Warning:{Colors.RESET} "
            f"Provider '{provider_id}' not found in models.dev API, skipping validation"
        )
        return whitelist
    
    # Calculate symmetric difference
    in_local_not_dev = sorted(local_models - models_dev_models)
    in_dev_not_local = sorted(models_dev_models - local_models)
    
    has_discrepancies = bool(in_local_not_dev or in_dev_not_local)
    
    if has_discrepancies:
        print(
            f"\n{Colors.YELLOW}{Colors.BOLD}⚠ Provider '{provider_id}' model discrepancy detected:{Colors.RESET}\n"
        )
        
        if in_local_not_dev:
            print(
                f"  {Colors.CYAN}Models in config but NOT in models.dev ({len(in_local_not_dev)}):{Colors.RESET}"
            )
            for model in in_local_not_dev[:10]:  # Limit output
                print(f"    {Colors.CYAN}• {model}{Colors.RESET}")
            if len(in_local_not_dev) > 10:
                print(f"    {Colors.CYAN}  ... and {len(in_local_not_dev) - 10} more{Colors.RESET}")
            print(
                f"\n  {Colors.BLUE}→ Action: Verify these models exist in 'opencode models {provider_id}' "
                f"and/or the provider's original API.{Colors.RESET}"
            )
            print(
                f"  {Colors.BLUE}  If confirmed, models.dev may be out of date.{Colors.RESET}\n"
            )
        
        if in_dev_not_local:
            print(
                f"  {Colors.MAGENTA}Models in models.dev but NOT in config ({len(in_dev_not_local)}):{Colors.RESET}"
            )
            for model in in_dev_not_local[:10]:  # Limit output
                print(f"    {Colors.MAGENTA}• {model}{Colors.RESET}")
            if len(in_dev_not_local) > 10:
                print(f"    {Colors.MAGENTA}  ... and {len(in_dev_not_local) - 10} more{Colors.RESET}")
            print(
                f"\n  {Colors.BLUE}→ Action: Check 'opencode models {provider_id}' for these models.{Colors.RESET}"
            )
            print(
                f"  {Colors.BLUE}  Add to whitelist (if free/usable) or blacklist in configs/providers/{provider_id}.json{Colors.RESET}\n"
            )
        
        # Show summary stats
        print(
            f"  {Colors.BOLD}Summary:{Colors.RESET} "
            f"local={len(local_models)} models.dev={len(models_dev_models)} "
            f"symmetric_diff={len(in_local_not_dev) + len(in_dev_not_local)}"
        )
    else:
        print(
            f"{Colors.GREEN}✓{Colors.RESET} Provider '{provider_id}' validated: "
            f"models.dev={len(models_dev_models)} whitelist={len(whitelist)} blacklist={len(blacklist)}"
        )
    
    return whitelist

# Cache for models.dev data
_models_dev_cache = None

def get_models_dev_provider_models(provider_id):
    """Get models for a provider from models.dev API (cached)."""
    global _models_dev_cache
    if _models_dev_cache is None:
        _models_dev_cache = fetch_models_dev_api()
    
    provider = _models_dev_cache.get(provider_id)
    if not provider:
        return None  # Provider not in models.dev
    return set((provider.get("models") or {}).keys())

# Test the validation
print(f"{Colors.BOLD}Testing opencode provider validation against models.dev...{Colors.RESET}")
assert_provider_partition_matches_models_dev("opencode")