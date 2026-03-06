#!/bin/bash
# GigaChat proxy startup script with auto-refresh token

set -e

ENV_FILE="${GIGACHAT_ENV_FILE:-$HOME/.openclaw/gigachat-new.env}"
PID_FILE="$HOME/.openclaw/gigachat.pid"
LOG_FILE="$HOME/.openclaw/gpt2giga.log"
PORT=8443

# Load credentials
if [ ! -f "$ENV_FILE" ]; then
  echo "Error: Environment file not found: $ENV_FILE"
  exit 1
fi

source "$ENV_FILE"

if [ -z "$GIGACHAT_CREDENTIALS" ]; then
  echo "Error: GIGACHAT_CREDENTIALS not set in $ENV_FILE"
  exit 1
fi

# Kill existing instance
if [ -f "$PID_FILE" ]; then
  OLD_PID=$(cat "$PID_FILE")
  kill "$OLD_PID" 2>/dev/null || true
  rm -f "$PID_FILE"
fi

# Cross-platform port cleanup
if command -v fuser >/dev/null 2>&1; then
  fuser -k $PORT/tcp 2>/dev/null || true
elif command -v lsof >/dev/null 2>&1; then
  pid=$(lsof -ti :$PORT 2>/dev/null)
  [ -n "$pid" ] && kill -9 $pid 2>/dev/null || true
fi
sleep 2

# Start gpt2giga using env vars (no tokens exposed on command line)
# gpt2giga natively reads GIGACHAT_CREDENTIALS, GIGACHAT_SCOPE, and
# GIGACHAT_VERIFY_SSL_CERTS from the environment — no manual OAuth needed.
echo "Starting gpt2giga proxy on port $PORT..."

# SSL verification: enable if Sber CA is installed, disable otherwise
SBER_CA="/etc/ssl/certs/sber-ca.crt"
if [ -f "$SBER_CA" ]; then
  export GIGACHAT_VERIFY_SSL_CERTS=true
else
  echo "⚠️  SSL verification disabled. Sber CA not found at $SBER_CA"
  echo "   To enable: download Sber root CA from https://developers.sber.ru/ and install to $SBER_CA"
  export GIGACHAT_VERIFY_SSL_CERTS=false
fi

# Export env vars for gpt2giga (credentials already loaded from ENV_FILE)
export GIGACHAT_CREDENTIALS
export GIGACHAT_SCOPE="${GIGACHAT_SCOPE:-GIGACHAT_API_PERS}"
export GPT2GIGA_HOST=127.0.0.1
export GPT2GIGA_PORT=$PORT

gpt2giga \
  --proxy.host 127.0.0.1 \
  --proxy.port $PORT \
  --proxy.pass-model true \
  > "$LOG_FILE" 2>&1 &

NEW_PID=$!
echo $NEW_PID > "$PID_FILE"

sleep 2

# Verify it's running
if ! kill -0 $NEW_PID 2>/dev/null; then
  echo "Error: gpt2giga failed to start"
  cat "$LOG_FILE" | tail -20
  exit 1
fi

echo "✅ gpt2giga started successfully (PID: $NEW_PID)"
echo "   Log: $LOG_FILE"
echo "   Endpoint: http://localhost:$PORT/v1/chat/completions"
echo ""
echo "⚠️  Token expires in ~30 minutes. Restart this script to refresh."
