---
name: yax
description: CLI tool for Yandex Disk, Calendar, and Mail via Yandex OAuth API
version: 1.4.0
metadata: {"openclaw":{"emoji":"📁","homepage":"https://github.com/smvlx/awesome-ru-ai-skills","os":["darwin","linux"],"requires":{"bins":["node"],"env":["YAX_CLIENT_ID"]},"primaryEnv":"YAX_CLIENT_ID","configPaths":["~/.openclaw/yax.env","~/.openclaw/yax-token.json"]}}
---

# yax — Yandex 360 CLI

CLI tool for Yandex Disk, Calendar, and Mail via Yandex OAuth API.

## Features

- **Disk**: info, list, mkdir, upload, download
- **Calendar**: list calendars, list events, create/update/delete events (via CalDAV)
- **Mail**: Full IMAP access via XOAUTH2 (list, read, delete emails, **attachments**)

## Prerequisites

1. Create a Yandex OAuth app at https://oauth.yandex.ru/client/new
   - Redirect URI: `https://oauth.yandex.ru/verification_code`
   - **Required scopes (критично для загрузки файлов):**
     - `cloud_api:disk.write` — ⚠️ Запись на диск (без этого НЕ работает upload!)
     - `cloud_api:disk.read` — Чтение информации о диске
     - `calendar:all` — Calendar read/write
     - `mail:imap_full` — Full IMAP access (read, delete)
     - `mail:smtp` — Mail sending via SMTP
   - Note the Client ID and Client Secret

2. Save config to `~/.openclaw/yax.env`:
   ```
   YAX_CLIENT_ID=your_app_client_id
   YAX_CLIENT_SECRET=your_app_secret_if_any
   ```

3. **После изменения scopes в приложении — обязательно переавторизуйся!**
   ```bash
   node src/yax.cjs auth
   ```

## Setup & Auth

```bash
scripts/setup.sh        # Create env template
node src/yax.cjs auth   # OAuth flow (opens browser URL, paste code)
```

## Usage

```bash
# Disk
node src/yax.cjs disk info
node src/yax.cjs disk list /
node src/yax.cjs disk mkdir /test-folder
node src/yax.cjs disk upload ./local-file.txt /remote-path.txt
node src/yax.cjs disk download /remote-path.txt ./local-file.txt

# Calendar
node src/yax.cjs calendar list                         # список календарей
node src/yax.cjs calendar list-events                  # события в календаре (UID + название + время)
node src/yax.cjs calendar create "Meeting" "2026-02-14" "11:00:00" "12:00:00" "Description" "Europe/Moscow"  # создать
node src/yax.cjs calendar update "<uid>" "New Title" "2026-02-14" "12:00:00" "13:00:00" "Desc" "Europe/Moscow"   # обновить
node src/yax.cjs calendar delete "<uid>"               # удалить

# Mail
node src/yax.cjs mail folders              # список папок
node src/yax.cjs mail list INBOX 10        # последние 10 писем
node src/yax.cjs mail read <uid>           # прочитать письмо
node src/yax.cjs mail delete <uid>         # удалить письмо
node src/yax.cjs mail send <to> <subject> <body>  # отправить письмо
node src/yax.cjs mail attachments <uid>    # список вложений в письме
node src/yax.cjs mail download <uid> "file.pdf"  # скачать одно вложение
node src/yax.cjs mail download_all <uid>  # скачать все вложения (в текущую папку)
```

## Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### [1.4.0] - 2026-04-21

#### Added
- `mail attachments <uid>` — list attachments in email
- `mail download <uid> "filename"` — download single attachment
- `mail download_all <uid>` — download all attachments from email
- IMAP attachment extraction via Python stdlib (`email` module)

### [1.3.0] - 2026-02-14

#### Added
- Full SMTP support for sending emails via XOAUTH2
- `mail send` command

### [1.2.0] - 2026-01-20

#### Added
- IMAP mail access (list, read, delete)
- `mail folders` command

### [1.1.0] - 2025-12-15

#### Added
- Calendar support via CalDAV
- Event CRUD operations

### [1.0.0] - 2025-11-01

#### Added
- Initial release
- Disk operations (info, list, mkdir, upload, download)

## Implementation Details

### Проблемы и решения

**Проблема:** `Upload URL error: { error: 'ForbiddenError' }`
**Причина:** OAuth-приложению не хватает scope `cloud_api:disk.write`
**Решение:** Добавь `cloud_api:disk.write` в scopes приложения на https://oauth.yandex.ru/client/your-app-id, затем переавторизуйся (`node src/yax.cjs auth`)

**Проблема:** Токен устарел / авторизация сбрасывается
**Решение:** Токен жив 1 год, но после изменения прав приложения нужна повторная авторизация. Старые токены остаются рабочими до истечения, но с новыми scopes — только после re-auth.

- **Calendar**: Uses raw CalDAV HTTP requests to `caldav.yandex.ru`. Automatically discovers user login via OAuth info endpoint and calendar paths via PROPFIND. Supports timezone-aware event creation. No external dependencies.
- **Mail**: IMAP via XOAUTH2 (no external deps). Uses Python stdlib `imaplib` + `email` modules. Requires `mail:imap_full` OAuth scope. Supports attachments extraction.

## Scripts

- `scripts/setup.sh` — Create env template
- `scripts/start.sh` — N/A (CLI tool, not a daemon)
- `scripts/stop.sh` — N/A
- `scripts/status.sh` — Check auth status
