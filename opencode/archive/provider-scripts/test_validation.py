#!/usr/bin/env python3
import sys
import json
import urllib.request

# Add current directory to path
sys.path.insert(0, '.')

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

# Test the models.dev API
print(f"{Colors.BOLD}Testing models.dev API validation...{Colors.RESET}")
try:
    api_data = fetch_models_dev_api()
    print(f"{Colors.GREEN}✓{Colors.RESET} Successfully fetched models.dev API")
    print(f"{Colors.BLUE}→ Found {len(api_data)} providers in models.dev{Colors.RESET}")
    
    # Show some example providers
    providers = list(api_data.keys())
    print(f"{Colors.CYAN}Sample providers:{Colors.RESET}")
    for i, provider in enumerate(providers[:5]):
        models = set((api_data[provider].get("models") or {}).keys())
        print(f"  • {provider}: {len(models)} models")
        
except Exception as e:
    print(f"{Colors.RED}✗{Colors.RESET} Error: {e}")
    sys.exit(1)

print(f"{Colors.GREEN}✓{Colors.RESET} models.dev API validation working correctly!")