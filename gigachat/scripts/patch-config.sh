#!/bin/bash
# Patch openclaw.json to add GigaChat provider
# Uses python3 (already required by this skill) instead of node
CONFIG="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"

if [ ! -f "$CONFIG" ]; then
  echo "Config not found: $CONFIG"
  exit 1
fi

# Back up config before patching
cp "$CONFIG" "${CONFIG}.bak"
echo "Backed up config to ${CONFIG}.bak"

python3 -c "
import json, sys
with open('$CONFIG') as f:
    cfg = json.load(f)
cfg.setdefault('providers', {})
cfg['providers']['gigachat'] = {
    'type': 'openai',
    'baseUrl': 'http://localhost:8443/v1',
    'apiKey': 'not-needed',
    'models': {
        'gigachat/GigaChat': {'id': 'GigaChat', 'aliases': ['gigachat']},
        'gigachat/GigaChat-Pro': {'id': 'GigaChat-Pro', 'aliases': ['gigachat-pro']},
        'gigachat/GigaChat-Max': {'id': 'GigaChat-Max', 'aliases': ['gigachat-max']}
    }
}
with open('$CONFIG', 'w') as f:
    json.dump(cfg, f, indent=2)
print('GigaChat provider added to', '$CONFIG')
"
