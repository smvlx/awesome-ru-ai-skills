# OpenClaw Russian AI Skills

Skills that give your AI coding agent access to Russian services: **GigaChat** (Sber), **YandexGPT**, **Yandex 360** (Disk, Calendar, Mail & Telemost), **Yandex Cloud**, and **Yandex Metrika**.

## What This Enables

Talk to your agent in natural language — it handles the rest:

| You say | Agent does |
|---------|----------|
| *"Answer in Russian using GigaChat-Max"* | Routes request through GigaChat proxy |
| *"Summarize this file with YandexGPT"* | Sends content through YandexGPT proxy |
| *"Upload report.pdf to Yandex Disk"* | Runs `yax disk upload` via CLI |
| *"Create a meeting tomorrow at 14:00"* | Runs `yax calendar create` with timezone |
| *"Deploy my static site to Object Storage"* | Runs `yc storage` commands |
| *"Check my Metrika stats for the last 30 days"* | Calls Metrika Reporting API |
| *"Create a DNS record for my domain"* | Runs `yc dns zone add-records` |
| *"Set up Metrika counter in my Next.js app"* | Generates tracking component code |

---

## Skills

| Skill | Directory | What it does |
|-------|-----------|-------------|
| **GigaChat** | `gigachat/` | Sber GigaChat API — Lite, Pro, Max models via OpenAI-compatible proxy |
| **YandexGPT** | `yandexgpt/` | Yandex Foundation Models — YandexGPT, Lite, 32K via proxy |
| **Yandex 360** | `yax/` | Disk, Calendar, Mail (IMAP/SMTP), Telemost via `yax` CLI |
| **Yandex Cloud** | `yandex-cloud/` | Full `yc` CLI reference — storage, compute, DNS, serverless, databases, certificates, and 30+ service groups |
| **Yandex Metrika** | `yandex-metrika/` | Analytics API — traffic stats, counters, goals, reports + Next.js setup guide |

---

## Installation

### Option 1: ClawHub (recommended)

Install each skill individually from ClawHub:

```bash
clawhub install smvlx/sber-gigachat
clawhub install smvlx/yandex-gpt
clawhub install smvlx/yandex-cli-yax
clawhub install smvlx/yandex-cloud
clawhub install smvlx/yandex-metrika
```

### Option 2: Install script

```bash
git clone https://github.com/smvlx/openclaw-ru-skills.git /tmp/openclaw-ru-skills
/tmp/openclaw-ru-skills/install.sh
```

This copies each skill into `~/.openclaw/skills/` and installs dependencies.

### Option 3: Manual install

```bash
git clone https://github.com/smvlx/openclaw-ru-skills.git
cp -r openclaw-ru-skills/gigachat ~/.openclaw/skills/
cp -r openclaw-ru-skills/yandexgpt ~/.openclaw/skills/
cp -r openclaw-ru-skills/yax ~/.openclaw/skills/
cp -r openclaw-ru-skills/yandex-cloud ~/.openclaw/skills/
cp -r openclaw-ru-skills/yandex-metrika ~/.openclaw/skills/
cd ~/.openclaw/skills/yax && npm install --omit=dev
```

### Option 4: Claude Code

For Claude Code users, copy the skill directories to `~/.claude/skills/`:

```bash
git clone https://github.com/smvlx/openclaw-ru-skills.git /tmp/openclaw-ru-skills
cp -r /tmp/openclaw-ru-skills/yandex-cloud ~/.claude/skills/
cp -r /tmp/openclaw-ru-skills/yandex-metrika ~/.claude/skills/
```

### Option 5: Chat-based install

Paste the repo URL into your agent conversation:

> Install skills from https://github.com/smvlx/openclaw-ru-skills

The agent will handle cloning and setup.

---

## Setup

Each skill needs **credentials from external services** — that's the only part you do manually. Everything else your agent handles.

### GigaChat (Sber AI)

<table>
<tr><td width="50%">

**You do once (2 min)**

1. Register at [developers.sber.ru](https://developers.sber.ru/)
2. Create a GigaChat API application
3. Copy **Client ID** and **Client Secret**
4. Choose scope: `GIGACHAT_API_PERS` (free) or `GIGACHAT_API_CORP` (paid)
5. Give credentials to your agent

</td><td width="50%">

**Agent automates**

```bash
# Create env file
cat > ~/.openclaw/gigachat-new.env << 'EOF'
CLIENT_ID="<your-id>"
CLIENT_SECRET="<your-secret>"
GIGACHAT_CREDENTIALS=$(echo -n "$CLIENT_ID:$CLIENT_SECRET" | base64)
GIGACHAT_SCOPE="GIGACHAT_API_PERS"
EOF

# Install proxy dependency
pip3 install gpt2giga

# Start proxy (localhost:8443)
start-proxy.sh
```

</td></tr>
</table>

**Models:** GigaChat Lite, GigaChat Pro, GigaChat MAX

---

### YandexGPT (Foundation Models)

<table>
<tr><td width="50%">

**You do once (3 min)**

1. Go to [Yandex Cloud Console](https://console.cloud.yandex.ru/iam)
2. Create a service account
3. Grant role `ai.languageModels.user`
4. Create an API key
5. Note your **Folder ID** and **API Key**
6. Give credentials to your agent

</td><td width="50%">

**Agent automates**

```bash
# Create env file
cat > ~/.openclaw/yandexgpt.env << 'EOF'
YANDEX_API_KEY="<your-api-key>"
YANDEX_FOLDER_ID="<your-folder-id>"
YANDEX_PROXY_PORT="8444"
EOF

# Start proxy (localhost:8444)
start.sh
```

</td></tr>
</table>

**Models:** YandexGPT Lite, YandexGPT, YandexGPT 32K

---

### Yandex 360 (Disk, Calendar, Mail & Telemost)

<table>
<tr><td width="50%">

**You do once (3 min)**

1. Create OAuth app at [oauth.yandex.ru/client/new](https://oauth.yandex.ru/client/new)
2. Set redirect URI: `https://oauth.yandex.ru/verification_code`
3. Enable scopes for the services you need:

   | Service | Scope |
   |---------|-------|
   | **Disk** | `cloud_api:disk.app_folder`, `cloud_api:disk.info` |
   | **Calendar** | `calendar:all` |
   | **Mail** | `mail:imap_full`, `mail:smtp` |
   | **Telemost** | `telemost-api:conferences.create` |

4. Note **Client ID**
5. Give credentials to your agent

</td><td width="50%">

**Agent automates**

```bash
# Authenticate (device code flow)
cd yax && node src/yax.cjs auth device
```

</td></tr>
</table>

---

### Yandex Cloud

<table>
<tr><td width="50%">

**You do once (2 min)**

1. Install `yc` CLI:
   ```bash
   curl -sSL https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash
   ```
2. Run `yc init` and follow the prompts
3. That's it — the skill uses the `yc` CLI directly

</td><td width="50%">

**Agent can do**

```bash
# Storage
yc storage bucket create --name my-site
yc storage s3 cp --recursive ./out/ s3://my-site/

# Compute
yc compute instance create --name my-vm ...

# DNS, certs, serverless, databases...
yc dns zone add-records ...
yc certificate-manager certificate request ...
yc serverless function create ...
```

</td></tr>
</table>

Covers 30+ service groups: storage, compute, VPC, DNS, certificates, managed databases (PostgreSQL, MySQL, ClickHouse, MongoDB, Redis, Kafka), Kubernetes, serverless, CDN, load balancers, and more.

---

### Yandex Metrika

<table>
<tr><td width="50%">

**You do once (3 min)**

1. Create an OAuth app at [oauth.yandex.com](https://oauth.yandex.com/?dialog=create-client-entry)
2. Add scopes: `metrika:read`, `metrika:write`
3. Generate a token via: `https://oauth.yandex.com/authorize?response_type=token&client_id=<app_id>`
4. Store the token (e.g. in `.env.local` as `YM_OAUTH_TOKEN`)

</td><td width="50%">

**Agent can do**

```bash
# Get traffic overview
curl -H 'Authorization: OAuth TOKEN' \
  'https://api-metrika.yandex.net/stat/v1/data?
  id=COUNTER_ID&metrics=ym:s:visits,ym:s:users
  &date1=30daysAgo&date2=today'

# Manage counters and goals
# Set up tracking in Next.js / React / HTML
# Build custom reports with 20+ metrics
```

</td></tr>
</table>

Includes: Management API (counters, goals), Reporting API (stats, time-series, comparisons), Next.js setup guide with SPA tracking.

---

## Architecture

```
                          AI Coding Agent

  "Use GigaChat"    "Use YandexGPT"    "Deploy to Cloud"    "Check Metrika"
       |                  |                   |                   |
       v                  v                   v                   v
 +-----------+    +------------+    +------------------+   +-------------+
 | gpt2giga  |    | Node.js    |    | yc CLI           |   | Metrika API |
 | proxy     |    | proxy      |    | (direct)         |   | (REST)      |
 | :8443     |    | :8444      |    |                  |   |             |
 +-----+-----+    +-----+------+    +--+-----+----+----+   +------+------+
       |                |              |     |    |               |
       v                v              v     v    v               v
   Sber API      Yandex Cloud      Storage  DNS  VMs     api-metrika.
   (OAuth)       Foundation        Compute  ...  ...     yandex.net
                 Models API
```

---

## Security

- Credentials stored locally with restrictive permissions
- Proxies bind to `127.0.0.1` only — no external access
- GigaChat tokens auto-refresh via OAuth (~30 min expiry)
- Yandex 360 uses OAuth device code flow — no passwords stored
- No tokens or secrets hardcoded in skill files

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| GigaChat `401 Unauthorized` | Token expired | Restart `start-proxy.sh` |
| GigaChat `402 Payment Required` | Quota exhausted | Switch model: Max -> Pro -> Lite |
| YandexGPT `403 Forbidden` | Wrong folder ID | Check `~/.openclaw/yandexgpt.env` |
| `yc: command not found` | CLI not in PATH | `export PATH="$HOME/yandex-cloud/bin:$PATH"` |
| `yc` unauthenticated | No token | Run `yc init` |
| Metrika 403 | Token missing scopes | Re-authorize with `metrika:read` scope |
| Metrika no data | Counter not firing | Check `code_status`, remove `ssr:true` from static exports |
| Yandex 360 token expired | OAuth refresh needed | Run `yax auth device` again |
| Mail IMAP/SMTP timeout | Ports blocked | Deploy on VPS or local machine |

---

## Detailed Documentation

Each skill has its own `SKILL.md` with full reference:

- [GigaChat SKILL.md](./gigachat/SKILL.md) — Token management, agent creation, model details
- [YandexGPT SKILL.md](./yandexgpt/SKILL.md) — Proxy internals, model URI mapping
- [Yandex 360 SKILL.md](./yax/SKILL.md) — Disk API, CalDAV, Mail, Telemost, OAuth flow
- [Yandex Cloud SKILL.md](./yandex-cloud/SKILL.md) — Full `yc` CLI reference, 30+ service groups
- [Yandex Metrika SKILL.md](./yandex-metrika/SKILL.md) — Management, Reporting & Logs APIs, Next.js setup

---

## Links

- **GigaChat API** — [developers.sber.ru/docs/ru/gigachat/overview](https://developers.sber.ru/docs/ru/gigachat/overview)
- **gpt2giga** — [pypi.org/project/gpt2giga](https://pypi.org/project/gpt2giga/)
- **YandexGPT API** — [cloud.yandex.ru/docs/foundation-models](https://cloud.yandex.ru/docs/foundation-models/)
- **Yandex Cloud CLI** — [cloud.yandex.ru/docs/cli](https://cloud.yandex.ru/docs/cli/)
- **Yandex Metrika API** — [yandex.ru/dev/metrika](https://yandex.ru/dev/metrika/)
- **Yandex OAuth** — [oauth.yandex.ru](https://oauth.yandex.ru/)

---

Created by [@smvlx](https://github.com/smvlx)
