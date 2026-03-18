# awesome-ru-ai-skills

AI agent skills for the Russian tech stack

[Версия на русском](./README.md)

![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-blue)
![OpenClaw](https://img.shields.io/badge/OpenClaw-compatible-blue)
![Any AI Agent](https://img.shields.io/badge/Any%20AI%20Agent-compatible-blue)

---

## What is this

A collection of skills for AI agents — integrations with Russian commercial services and platforms: Yandex, Sber, Bitrix24, 1C, amoCRM, and others.

---

## Skills

| Skill | Description | Platforms | Author |
|-------|-------------|-----------|--------|
| 🤖 [gigachat](./skills/gigachat/) | GigaChat (Sber) via gpt2giga proxy | CC · OC | [@smvlx](https://github.com/smvlx) |
| 🦊 [yandexgpt](./skills/yandexgpt/) | YandexGPT — Yandex Foundation Models | CC · OC | [@smvlx](https://github.com/smvlx) |
| 📁 [yax](./skills/yax/) | Yandex 360: Disk, Calendar, Mail, Telemost | CC · OC | [@smvlx](https://github.com/smvlx) |
| ☁️ [yandex-cloud](./skills/yandex-cloud/) | Yandex Cloud infrastructure (yc CLI) | CC · OC | [@smvlx](https://github.com/smvlx) |
| 📊 [yandex-metrika](./skills/yandex-metrika/) | Yandex Metrika web analytics | CC · OC | [@smvlx](https://github.com/smvlx) |
| _bitrix24_ | _Bitrix24 CRM API_ | — | _open for PR_ |
| _amocrm_ | _amoCRM / Kommo API_ | — | _open for PR_ |

CC = Claude Code · OC = OpenClaw · _italics = waiting for contributions_

---

## Installation

```bash
git clone https://github.com/smvlx/awesome-ru-ai-skills.git ~/awesome-ru-ai-skills
~/awesome-ru-ai-skills/install.sh
```

Or install a single skill manually:

```bash
cp -r skills/gigachat ~/.openclaw/skills/
```

---

## Contribute

Open a PR — add a row to the table or source code in `skills/`. See [CONTRIBUTING.en.md](./CONTRIBUTING.en.md).

---

Made by [@smvlx](https://habr.com/ru/users/smvlx/) on Habr · [@smirnov_sasha](https://www.threads.net/@smirnov_sasha) on Threads · MIT License
