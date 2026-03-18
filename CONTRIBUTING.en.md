# How to Contribute

Версия на русском: [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## What We Accept

Skills for AI agents that integrate with Russian commercial services and platforms: Yandex, Sber, Bitrix24, 1C, amoCRM, and others.

---

## How to Add a Skill

**Option 1 — source in this repo:**

Add your skill folder to `skills/` and open a PR.

**Option 2 — external repo:**

Add a row to the table in `README.md` linking to your repo. No need to include source code here.

---

## Table Row Template

Add a row to the `## Скиллы / Skills` table in `README.md`:

```markdown
| 🔧 your-skill-name | One-line description | CC · OC | @your-handle |
```

Columns:
- **Skill** — name + link (to folder in this repo or to external repo)
- **Description** — one line, ideally in Russian (the primary audience)
- **Platforms** — `CC` (Claude Code), `OC` (OpenClaw), or others
- **Author** — your GitHub handle

---

## Skill Requirements

Every skill must have a `SKILL.md` with frontmatter:

```yaml
---
name: your-skill-name
description: One line — what the skill does
version: 1.0.0
---
```

---

## Process

1. Fork the repo
2. Make your changes
3. Open a PR
4. Review by @smvlx
5. Merge

Questions? Reach out on Threads: [@smirnov_sasha](https://www.threads.net/@smirnov_sasha)
