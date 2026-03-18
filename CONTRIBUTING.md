# Как добавить скилл / How to Contribute

---

## Что принимаем / What We Accept

Скиллы для AI-агентов, которые интегрируются с российскими сервисами и платформами: Яндекс, Сбер, Bitrix24, 1С, amoCRM, Госуслуги, и другими.

_Skills for AI agents that integrate with Russian services and platforms: Yandex, Sber, Bitrix24, 1C, amoCRM, Gosuslugi, and others._

---

## Как добавить скилл / How to Add a Skill

**Вариант 1 — исходники в этом репо / Option 1 — source in this repo:**

Добавьте папку со скиллом в `skills/` и откройте PR.

_Add your skill folder to `skills/` and open a PR._

**Вариант 2 — внешнее репо / Option 2 — external repo:**

Добавьте строку в таблицу в `README.md`, указав ссылку на ваш репо. Открывать PR с исходниками не нужно.

_Add a row to the table in `README.md` linking to your repo. No need to include source code here._

---

## Шаблон строки в таблице / Table Row Template

Добавьте строку в таблицу `## Скиллы / Skills` в `README.md`:

```markdown
| 🔧 your-skill-name | Описание скилла на русском | CC · OC | @your-handle |
```

Колонки / Columns:
- **Скилл** — название + ссылка (на папку в этом репо или на внешний репо)
- **Описание** — одна строка на русском
- **Платформы** — `CC` (Claude Code), `OC` (OpenClaw), или другие
- **Автор** — ваш GitHub handle

---

## Требования к скиллу / Skill Requirements

Скилл должен содержать файл `SKILL.md` с frontmatter:

```yaml
---
name: your-skill-name
description: Одна строка — что делает скилл
version: 1.0.0
---
```

_Every skill must have a `SKILL.md` with name, description, and version in the frontmatter._

---

## Процесс / Process

1. Форкните репо / Fork the repo
2. Внесите изменения / Make your changes
3. Откройте PR / Open a PR
4. Ревью от @smvlx / Review by @smvlx
5. Мёрдж / Merge

Вопросы? Пишите в Threads: [@smirnov_sasha](https://www.threads.net/@smirnov_sasha)

_Questions? Reach out on Threads: [@smirnov_sasha](https://www.threads.net/@smirnov_sasha)_
