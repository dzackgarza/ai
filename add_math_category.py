#!/usr/bin/env python3
"""Add 'math' category to existing math-related engines."""
import yaml

with open('/etc/searxng/settings.yml', 'r') as f:
    config = yaml.safe_load(f)

# Add custom 'math' category
if 'categories_as_tabs' not in config:
    config['categories_as_tabs'] = {}
config['categories_as_tabs']['math'] = {}

# EXISTING engines to add to math category
# These are confirmed to exist and be enabled
math_engines = [
    'mathoverflow',
    'math.stackexchange', 
    'arxiv',
    'openlibrary',
    'library genesis',
]

if 'engines' not in config:
    config['engines'] = []

for engine_name in math_engines:
    existing = [e for e in config['engines'] if e.get('name') == engine_name]
    
    if existing:
        eng = existing[0]
        cats = eng.get('categories', [])
        if isinstance(cats, str):
            cats = [cats]
        if 'math' not in cats:
            cats.append('math')
            eng['categories'] = cats
            print(f'Added "math" to {engine_name}')
    else:
        # Engine not in settings.yml - add minimal enable entry
        config['engines'].append({
            'name': engine_name,
            'categories': ['math'],
            'disabled': False,
        })
        print(f'Enabled {engine_name} in "math" category')

with open('/etc/searxng/settings.yml', 'w') as f:
    yaml.dump(config, f, default_flow_style=False, sort_keys=False)

print('Done.')
