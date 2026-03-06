#!/usr/bin/env python3
import yaml

with open('/etc/searxng/settings.yml', 'r') as f:
    config = yaml.safe_load(f)

if 'engines' not in config:
    config['engines'] = []

# Add mathoverflow if not exists
mo_existing = [e for e in config['engines'] if e.get('name') == 'mathoverflow']
if not mo_existing:
    config['engines'].append({
        'name': 'mathoverflow',
        'engine': 'stackexchange',
        'api_site': 'mathoverflow',
        'categories': 'science',
        'shortcut': '!mo',
        'disabled': False
    })
    print('Added mathoverflow engine')

# Add math.stackexchange if not exists
mse_existing = [e for e in config['engines'] if e.get('name') == 'math.stackexchange']
if not mse_existing:
    config['engines'].append({
        'name': 'math.stackexchange',
        'engine': 'stackexchange',
        'api_site': 'math.stackexchange',
        'categories': 'science',
        'shortcut': '!mse',
        'disabled': False
    })
    print('Added math.stackexchange engine')

with open('/etc/searxng/settings.yml', 'w') as f:
    yaml.dump(config, f, default_flow_style=False, sort_keys=False)

print('Done')
