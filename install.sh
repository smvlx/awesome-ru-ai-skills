#!/usr/bin/env bash
set -euo pipefail

SKILLS_DIR="${OPENCLAW_SKILLS_DIR:-$HOME/.openclaw/skills}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS=(gigachat yandexgpt yax yandex-cloud yandex-metrika)

echo "Installing awesome-ru-ai-skills to $SKILLS_DIR ..."

mkdir -p "$SKILLS_DIR"

for skill in "${SKILLS[@]}"; do
  src="$SCRIPT_DIR/skills/$skill"
  dest="$SKILLS_DIR/$skill"

  if [ ! -d "$src" ]; then
    echo "  skip: $skill (not found in repo)"
    continue
  fi

  if [ -d "$dest" ]; then
    echo "  update: $skill"
    rm -rf "$dest"
  else
    echo "  install: $skill"
  fi

  cp -r "$src" "$dest"

  # Run npm install if package.json exists
  if [ -f "$dest/package.json" ]; then
    echo "  deps: $skill (npm install)"
    (cd "$dest" && npm install --omit=dev --silent)
  fi
done

echo "Done. Restart your AI agent to pick up the new skills."
