# awesome-ru-ai-skills

Скиллы для AI-агентов: российский технологический стек

_AI agent skills for the Russian tech stack_

![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-blue)
![OpenClaw](https://img.shields.io/badge/OpenClaw-compatible-blue)
![Any AI Agent](https://img.shields.io/badge/Any%20AI%20Agent-compatible-blue)

---

## Что это

Подборка скиллов для AI-агентов — интеграции с российскими сервисами и платформами: Яндекс, Сбер, Bitrix24, 1С, amoCRM и другими.

_A collection of AI agent skills — integrations with Russian services and platforms._

---

## Скиллы / Skills

| Скилл | Описание | Платформы | Автор |
|-------|----------|-----------|-------|
| 🤖 [gigachat](./skills/gigachat/) | GigaChat (Сбер) через gpt2giga прокси | CC · OC | [@smvlx](https://github.com/smvlx) |
| 🦊 [yandexgpt](./skills/yandexgpt/) | YandexGPT — Yandex Foundation Models | CC · OC | [@smvlx](https://github.com/smvlx) |
| 📁 [yax](./skills/yax/) | Яндекс 360: Диск, Календарь, Почта, Телемост | CC · OC | [@smvlx](https://github.com/smvlx) |
| ☁️ [yandex-cloud](./skills/yandex-cloud/) | Инфраструктура Яндекс Облака (yc CLI) | CC · OC | [@smvlx](https://github.com/smvlx) |
| 📊 [yandex-metrika](./skills/yandex-metrika/) | Яндекс Метрика — веб-аналитика | CC · OC | [@smvlx](https://github.com/smvlx) |
| _bitrix24_ | _Bitrix24 CRM API_ | — | _открыто для PR_ |
| _amocrm_ | _amoCRM / Kommo API_ | — | _открыто для PR_ |

CC = Claude Code · OC = OpenClaw · _курсив = ждём PR / waiting for contributions_

---

## Установка / Installation

```bash
git clone https://github.com/smvlx/awesome-ru-ai-skills.git ~/awesome-ru-ai-skills
~/awesome-ru-ai-skills/install.sh
```

Или установите отдельный скилл вручную / Or install a single skill manually:

```bash
cp -r skills/gigachat ~/.openclaw/skills/
```

---

## Добавить скилл / Contribute

Откройте PR — добавьте строку в таблицу или исходники в `skills/`. Подробности в [CONTRIBUTING.md](./CONTRIBUTING.md).

_Open a PR — add a row to the table or source code in `skills/`. See [CONTRIBUTING.md](./CONTRIBUTING.md)._

---

Сделано [@smvlx](https://habr.com/ru/users/smvlx/) на Habr · [@smirnov_sasha](https://www.threads.net/@smirnov_sasha) в Threads · MIT License
