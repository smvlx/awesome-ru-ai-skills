#!/bin/bash
set -e

ENV_FILE="${GIGACHAT_ENV_FILE:-$HOME/.openclaw/gigachat.env}"
PID_FILE="$HOME/.openclaw/gigachat.pid"
LOG_FILE="$HOME/.openclaw/gpt2giga.log"

if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "gpt2giga already running (PID $(cat "$PID_FILE"))"
  exit 0
fi

if [ ! -f "$ENV_FILE" ]; then
  echo "Error: env file not found at $ENV_FILE"
  exit 1
fi

source "$ENV_FILE"

# SSL verification: enable if Sber CA is installed, disable otherwise
SBER_CA="/etc/ssl/certs/sber-ca.crt"
if [ -f "$SBER_CA" ]; then
  export GIGACHAT_VERIFY_SSL_CERTS=true
else
  echo "⚠️  SSL verification disabled. Sber CA not found at $SBER_CA"
  echo "   To enable: download Sber root CA from https://developers.sber.ru/ and install to $SBER_CA"
  export GIGACHAT_VERIFY_SSL_CERTS=false
fi

export GIGACHAT_CREDENTIALS
export GIGACHAT_SCOPE="${GIGACHAT_SCOPE:-GIGACHAT_API_PERS}"

nohup gpt2giga \
  --proxy.host 127.0.0.1 \
  --proxy.port 8443 \
  --proxy.pass-model true \
  > "$LOG_FILE" 2>&1 &

echo $! > "$PID_FILE"
echo "gpt2giga started on port 8443 (PID $!)"
sleep 2
