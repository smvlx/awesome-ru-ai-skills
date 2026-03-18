# Repo Restructure Design: awesome-ru-ai-skills

**Date:** 2026-03-18
**Author:** @smvlx
**Status:** Approved

---

## Summary

Rebrand and restructure `openclaw-ru-skills` into `awesome-ru-ai-skills` — a public, community-driven collection of AI agent skills for integrating with Russian tech stack platforms (Yandex, Sber, Bitrix24, 1C, amoCRM, etc.). Platform-agnostic: skills work on Claude Code, OpenClaw, and any AI agent that reads skill files.

---

## Goals

- Broaden scope beyond OpenClaw to universal AI agent skills
- Shift positioning from "Russian-speaking agents" to "Russian tech stack integrations"
- Open to community contributions (curated PR model)
- Establish personal brand: @smvlx on Habr, @smirnov_sasha on Threads
- Bilingual: Russian primary, English secondary for SEO and international reach

---

## New Repo Identity

**Name:** `awesome-ru-ai-skills`
**Tagline (RU):** Скиллы для AI-агентов: российский технологический стек
**Tagline (EN):** AI agent skills for the Russian tech stack
**Description (RU):** Подборка скиллов для AI-агентов — интеграции с российскими сервисами и платформами: Яндекс, Сбер, Bitrix24, 1С, amoCRM и другими.
**License:** MIT
**Visibility:** Public

No Russian flag emoji — "ru" reads as a country-code suffix, neutral and internationally understood.

---

## Folder Structure

```
awesome-ru-ai-skills/
├── skills/
│   ├── gigachat/          # GigaChat (Sber) via gpt2giga proxy
│   ├── yandexgpt/         # YandexGPT Foundation Models
│   ├── yax/               # Yandex 360: Disk, Calendar, Mail, Telemost
│   ├── yandex-cloud/      # Yandex Cloud infra via yc CLI (moved from ~/.claude)
│   └── yandex-metrika/    # Yandex Metrika analytics (moved from ~/.claude)
├── docs/
│   └── superpowers/specs/ # Design docs
├── README.md              # Bilingual, skills table
├── CONTRIBUTING.md        # How to add a skill
├── install.sh             # Updated paths
└── .gitignore
```

**Migration:** existing `gigachat/`, `yandexgpt/`, `yax/` move into `skills/`. The Claude Code skills `yandex-cloud` and `yandex-metrika` are copied here as the canonical source.

---

## README Structure

1. **Header** — repo name, RU tagline, EN subtitle, platform badges (Claude Code · OpenClaw · Any AI Agent)
2. **Что это / What is this** — RU description + EN italic subtitle
3. **Скиллы / Skills** — table with columns: Скилл · Описание · Платформы · Автор. Includes placeholder rows for Bitrix24 and amoCRM marked "открыто для PR" to signal community opportunity.
4. **Добавить скилл / Contribute** — RU instructions + EN italic, links to CONTRIBUTING.md
5. **Footer** — `Сделано @smvlx на Habr · @smirnov_sasha в Threads · MIT License`

Platform badges in table: `CC` = Claude Code, `OC` = OpenClaw.
Ghost rows for wanted-but-missing skills drive contributor discovery.

---

## Contributor Model

**Curated list (Option A) with hybrid source:**
- Author's skills: full source lives in `/skills/` in this repo
- Community skills: contributors add a row to the README table linking to their own repo
- PR review by @smvlx before merge
- `CONTRIBUTING.md` defines the template: name, description, platform compatibility, link or source

---

## Platform Compatibility

All skills are universal — they work on any AI agent that reads skill files. Each skill's `SKILL.md` frontmatter will include a `platforms` field listing supported agents. No platform-specific subdirectories needed.

---

## Files to Create/Update

| File | Action |
|------|--------|
| `README.md` | Full rewrite — bilingual, new identity |
| `CONTRIBUTING.md` | New — bilingual (RU primary, EN secondary), see structure below |
| `install.sh` | Four specific changes — see below |
| `skills/gigachat/` | Move from `gigachat/` |
| `skills/yandexgpt/` | Move from `yandexgpt/` |
| `skills/yax/` | Move from `yax/` |
| `skills/yandex-cloud/` | Add — source: `~/.claude/plugins/cache/*/skills/yandex-cloud/` |
| `skills/yandex-metrika/` | Add — source: `~/.claude/plugins/cache/*/skills/yandex-metrika/` |
| `.gitignore` | Already updated (`.superpowers/` added) |

### install.sh — required changes

1. `SKILLS=(gigachat yandexgpt yax)` → add `yandex-cloud` and `yandex-metrika`
2. `src="$SCRIPT_DIR/$skill"` → `src="$SCRIPT_DIR/skills/$skill"`
3. User-facing echo text: remove references to `openclaw-ru-skills`, make platform-agnostic
4. Final message: `"Done. Restart OpenClaw..."` → `"Done. Restart your AI agent to pick up the new skills."`

### CONTRIBUTING.md — required sections

Bilingual: RU primary, EN italic secondary (same convention as README).

1. **Что принимаем / What we accept** — skills that integrate with Russian tech stack platforms
2. **Как добавить скилл / How to add a skill** — two paths:
   - Source in this repo: add folder to `skills/`, open PR
   - External repo: add a row to the README table only, open PR
3. **Шаблон строки в таблице / Table row template** — columns: Скилл (name + link) · Описание (RU) · Платформы (CC/OC/etc.) · Автор (@handle)
4. **Требования к скиллу / Skill requirements** — must have a `SKILL.md` with name, description, and platform compatibility in frontmatter
5. **Процесс / Process** — open PR → review by @smvlx → merge

---

## Out of Scope

- Creating Bitrix24, 1C, or amoCRM skills (placeholder rows only — community contribution)
- GitHub Actions / CI for skill validation
- Automated install via package manager
- Versioned releases (future milestone)
