#!/usr/bin/env python3

import json
import urllib.request

def fetch_models_dev_api():
    url = "https://models.dev/api.json"
    req = urllib.request.Request(url, headers={"User-Agent": "opencode-config-builder/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode())

api_data = fetch_models_dev_api()
opencode_data = api_data.get("opencode")

if opencode_data:
    print(f"models.dev shows opencode provider with {len(opencode_data['models'])} models:")
    print()
    for model_id, model_info in opencode_data['models'].items():
        print(f"  {model_id} - {model_info['name']}")
else:
    print("opencode provider not found in models.dev")
    
    # Check if there are similar provider names
    similar = [p for p in api_data.keys() if 'open' in p.lower() or 'code' in p.lower()]
    print(f"\nSimilar provider names: {similar}")