#!/usr/bin/env python3

import json
import urllib.request
import sys

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
    url = "https://models.dev/api.json"
    req = urllib.request.Request(url, headers={"User-Agent": "opencode-config-builder/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode())

def assert_provider_partition_matches_models_dev(provider_id, provider_cfg):
    """Validate provider config against models.dev canonical source."""
    
    whitelist = set((provider_cfg.get("models") or {}).keys())
    blacklist = set(provider_cfg.get("blacklist") or [])
    
    # Check for overlap
    overlap = sorted(whitelist & blacklist)
    if overlap:
        print(f"  {Colors.RED}{Colors.BOLD}❌ ERROR:{Colors.RESET} Models in both whitelist and blacklist: {overlap}")
        return None

    local_models = whitelist | blacklist
    models_dev_models = get_models_dev_provider_models(provider_id)
    
    # Provider not in models.dev
    if models_dev_models is None:
        print(f"  {Colors.YELLOW}{Colors.BOLD}⚠️  WARNING:{Colors.RESET} Provider '{provider_id}' not found in models.dev API")
        return whitelist
    
    # Calculate symmetric difference
    in_local_not_dev = sorted(local_models - models_dev_models)
    in_dev_not_local = sorted(models_dev_models - local_models)
    
    has_discrepancies = bool(in_local_not_dev or in_dev_not_local)
    
    if has_discrepancies:
        print(f"\n  {Colors.YELLOW}{Colors.BOLD}⚠️  DISCREPANCY DETECTED for '{provider_id}':{Colors.RESET}")
        
        if in_local_not_dev:
            print(f"    {Colors.CYAN}Models in config but NOT in models.dev ({len(in_local_not_dev)}):{Colors.RESET}")
            for model in in_local_not_dev[:5]:  # Limit output
                print(f"      {Colors.CYAN}• {model}{Colors.RESET}")
            if len(in_local_not_dev) > 5:
                print(f"      {Colors.CYAN}  ... and {len(in_local_not_dev) - 5} more{Colors.RESET}")
        
        if in_dev_not_local:
            print(f"    {Colors.MAGENTA}Models in models.dev but NOT in config ({len(in_dev_not_local)}):{Colors.RESET}")
            for model in in_dev_not_local[:5]:  # Limit output
                print(f"      {Colors.MAGENTA}• {model}{Colors.RESET}")
            if len(in_dev_not_local) > 5:
                print(f"      {Colors.MAGENTA}  ... and {len(in_dev_not_local) - 5} more{Colors.RESET}")
        
        # Show summary stats
        print(f"    {Colors.BOLD}Summary:{Colors.RESET} local={len(local_models)} models.dev={len(models_dev_models)} symmetric_diff={len(in_local_not_dev) + len(in_dev_not_local)}")
        print(f"    {Colors.BLUE}→ Action needed: Review and resolve discrepancies{Colors.RESET}")
    else:
        print(f"  {Colors.GREEN}✓{Colors.RESET} Provider '{provider_id}' validated: models.dev={len(models_dev_models)} whitelist={len(whitelist)} blacklist={len(blacklist)}")
    
    return whitelist

# Cache for models.dev data
_models_dev_cache = None

def get_models_dev_provider_models(provider_id):
    global _models_dev_cache
    if _models_dev_cache is None:
        _models_dev_cache = fetch_models_dev_api()
    
    provider = _models_dev_cache.get(provider_id)
    if not provider:
        return None
    return set((provider.get("models") or {}).keys())

# Load current config
config = {}
try:
    with open("/home/dzack/ai/opencode/opencode.json", "r") as f:
        config = json.load(f)
except:
    # Try to build config first
    import subprocess
    subprocess.run(["python3", "build_config.py"], check=True)
    with open("/home/dzack/ai/opencode/opencode.json", "r") as f:
        config = json.load(f)

# Test all providers
providers = config.get("provider", {})
print(f"{Colors.BOLD}{Colors.BLUE}Validating all providers against models.dev:{Colors.RESET}")
print(f"{Colors.BOLD}Total providers to check: {len(providers)}{Colors.RESET}")
print()

providers_with_discrepancies = 0
providers_validated = 0

for provider_id, provider_cfg in providers.items():
    print(f"{Colors.BOLD}{Colors.WHITE}Provider: {provider_id}{Colors.RESET}")
    try:
        result = assert_provider_partition_matches_models_dev(provider_id, provider_cfg)
        if result is not None:
            providers_validated += 1
            if "DISCREPANCY DETECTED" in str(result):
                providers_with_discrepancies += 1
    except Exception as e:
        print(f"  {Colors.RED}{Colors.BOLD}❌ ERROR: {e}{Colors.RESET}")
    print()

# Summary
print(f"{Colors.BOLD}{Colors.BLUE}VALIDATION SUMMARY:{Colors.RESET}")
print(f"{Colors.GREEN}✓{Colors.RESET} Providers validated: {providers_validated}")
print(f"{Colors.YELLOW}⚠{Colors.RESET} Providers with discrepancies: {providers_with_discrepancies}")
print(f"{Colors.BOLD}Total models.dev sources checked: {len(providers)}{Colors.RESET}")