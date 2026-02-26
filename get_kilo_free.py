import json
import subprocess
import os

config_path = '.opencode/opencode.json'
bak_path = '.opencode/opencode.json.bak2'

# Backup
with open(config_path, 'r') as f:
    config = json.load(f)

with open(bak_path, 'w') as f:
    json.dump(config, f, indent=2)

# Clear restrictions
if 'provider' in config:
    for p in config['provider']:
        if 'blacklist' in config['provider'][p]:
            config['provider'][p]['blacklist'] = []

if 'disabled_providers' in config:
    config['disabled_providers'] = []

# Save temp config
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

# Run kilo models
print("Running kilo models...")
res = subprocess.run(['kilo', 'models'], capture_output=True, text=True)
free_models = [line.strip() for line in res.stdout.split('\n') if ':free' in line]
print("\n".join(free_models))

# Restore backup
with open(bak_path, 'r') as f:
    orig_config = json.load(f)
with open(config_path, 'w') as f:
    json.dump(orig_config, f, indent=2)
