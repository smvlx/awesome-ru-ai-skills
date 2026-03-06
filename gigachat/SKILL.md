---
name: gigachat
description: Integrate GigaChat (Sber AI) with OpenClaw via gpt2giga proxy
version: 1.2.0
metadata: {"openclaw":{"emoji":"🤖","homepage":"https://github.com/smvlx/openclaw-ru-skills","os":["darwin","linux"],"requires":{"bins":["python3","curl"],"env":["GIGACHAT_CREDENTIALS","GIGACHAT_SCOPE"]},"primaryEnv":"GIGACHAT_CREDENTIALS","configPaths":["~/.openclaw/gigachat-new.env","~/.openclaw/openclaw.json"],"install":[{"type":"uv","package":"gpt2giga"}]}}
---

# GigaChat Skill

Integrate GigaChat (Sber AI) with OpenClaw via gpt2giga proxy.

## Features

- Three models: GigaChat, GigaChat-Pro, GigaChat-Max
- OpenAI API compatibility via gpt2giga proxy
- Automatic token management (gpt2giga handles OAuth internally)
- Credentials passed via environment variables only (never on CLI)

## Prerequisites

1. **GigaChat API Access**:
   - Register at https://developers.sber.ru/
   - Create a GigaChat API application
   - Note your Client ID and Client Secret
   - Choose scope: `GIGACHAT_API_PERS` (free tier) or `GIGACHAT_API_CORP` (paid)

2. **Python & gpt2giga**:

   ```bash
   pip3 install gpt2giga
   ```

3. **Environment File**:
   Create `~/.openclaw/gigachat-new.env`:

   ```bash
   CLIENT_ID="your-client-id-here"
   CLIENT_SECRET="your-client-secret-here"

   # Auto-generate credentials (base64 of CLIENT_ID:CLIENT_SECRET)
   GIGACHAT_CREDENTIALS=$(echo -n "$CLIENT_ID:$CLIENT_SECRET" | base64)
   GIGACHAT_SCOPE="GIGACHAT_API_PERS"
   ```

## Quick Start

### 1. Start the proxy

```bash
/openclaw/skills/gigachat/scripts/start-proxy.sh
```

Output:

```
Starting gpt2giga proxy on port 8443...
✅ gpt2giga started successfully (PID: 12345)
   Log: ~/.openclaw/gpt2giga.log
   Endpoint: http://localhost:8443/v1/chat/completions
```

gpt2giga handles OAuth token generation and refresh internally using the `GIGACHAT_CREDENTIALS` environment variable.

### 2. Configure OpenClaw

Run the patch script (backs up your config first):

```bash
/openclaw/skills/gigachat/scripts/patch-config.sh
```

Or add manually to `openclaw.json`:

```json
{
  "models": {
    "providers": {
      "gigachat": {
        "baseUrl": "http://127.0.0.1:8443",
        "apiKey": "not-needed",
        "api": "openai-completions",
        "models": [
          {
            "id": "GigaChat-Max",
            "name": "GigaChat MAX",
            "contextWindow": 32768,
            "maxTokens": 8192
          },
          {
            "id": "GigaChat-Pro",
            "name": "GigaChat Pro",
            "contextWindow": 32768,
            "maxTokens": 4096
          },
          {
            "id": "GigaChat",
            "name": "GigaChat Lite",
            "contextWindow": 8192,
            "maxTokens": 2048
          }
        ]
      }
    }
  }
}
```

### 3. Test

```bash
curl -s -X POST http://localhost:8443/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "GigaChat-Max",
    "messages": [{"role": "user", "content": "Привет!"}]
  }' | jq -r '.choices[0].message.content'
```

Expected output:

```
Привет! Как дела?
```

## Creating an Agent

Add a GigaChat-powered agent to `openclaw.json`:

```json
{
  "agents": {
    "list": [
      {
        "id": "ruslan",
        "name": "Ruslan",
        "emoji": "🐻",
        "model": "gigachat/GigaChat-Pro",
        "workspace": "/root/.openclaw/agents/ruslan/workspace"
      }
    ]
  }
}
```

Create agent workspace:

```bash
mkdir -p /root/.openclaw/agents/ruslan/workspace
```

**IDENTITY.md**:

```markdown
# IDENTITY.md

- Name: Ruslan
- Creature: Российский AI-ассистент
- Vibe: Дружелюбный, знает русский контекст
- Emoji: 🐻
```

**SOUL.md**:

```markdown
# SOUL.md — Кто ты

Ты Руслан. Российский AI-ассистент на базе GigaChat.

Говоришь на русском, знаешь русский контекст (кухня, культура, реалии).
Отвечаешь кратко и по делу. Без лишней вежливости.
```

## Token Management

gpt2giga handles OAuth token generation and refresh automatically using the `GIGACHAT_CREDENTIALS` environment variable. No manual token management is needed.

If the proxy loses its token (e.g. after a long idle period), restart it:

```bash
/openclaw/skills/gigachat/scripts/start-proxy.sh
```

## Troubleshooting

### Issue: 401 Unauthorized

**Cause:** Token expired or invalid credentials  
**Fix:** Restart proxy script (generates fresh token)

### Issue: 402 Payment Required

**Cause:** Quota exhausted for that model  
**Fix:** Try a different model or wait for quota reset

- Free tier: Limits per model
- Strategy: Rotate between Max → Pro → Lite

### Issue: Process defunct / zombie

**Cause:** gpt2giga crashes but holds port  
**Fix:**

```bash
fuser -k 8443/tcp
/openclaw/skills/gigachat/scripts/start-proxy.sh
```


## Architecture

```
OpenClaw → http://localhost:8443/v1/chat/completions
           ↓
       gpt2giga (proxy, env-var auth)
           ↓
   Sber GigaChat API (OAuth token auto-managed)
```

**Flow:**

1. Startup script exports credentials as environment variables
2. gpt2giga starts and handles OAuth token generation internally
3. OpenClaw sends OpenAI-format requests to localhost:8443
4. gpt2giga translates to GigaChat format and manages auth
5. Responses translated back to OpenAI format

## Files

- `scripts/start-proxy.sh` — Start proxy with env-var credentials
- `scripts/start.sh` — Alternative start (nohup)
- `scripts/stop.sh` — Stop proxy
- `scripts/status.sh` — Check proxy status
- `scripts/setup.sh` — Install gpt2giga from PyPI
- `scripts/patch-config.sh` — Add GigaChat provider to openclaw.json (backs up config first)
- `SKILL.md` — This file

## Limitations

- **Free Tier Quotas:** Limited tokens per model
- **SSL Verification:** Disabled by default due to Sber's custom CA; install Sber root CA to `/etc/ssl/certs/sber-ca.crt` to enable
- **Credentials:** Passed via environment variables only (never on the command line); protect `~/.openclaw/gigachat-new.env` with `chmod 600`

## References

- GigaChat Docs: https://developers.sber.ru/docs/ru/gigachat/overview
- gpt2giga: https://pypi.org/project/gpt2giga/
- OpenClaw: https://openclaw.ai
