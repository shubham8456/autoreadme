#!/bin/sh
set -eu

ollama serve >/tmp/ollama.log 2>&1 &
OLLAMA_PID=$!

cleanup() {
  kill "$OLLAMA_PID" >/dev/null 2>&1 || true
}
trap cleanup EXIT INT TERM

READY=0
for _ in $(seq 1 60); do
  if curl -fsS "${AUTOREADME_OLLAMA_URL}/api/tags" >/dev/null 2>&1; then
    READY=1
    break
  fi
  sleep 1
done

if [ "$READY" -ne 1 ]; then
  echo "Ollama failed to start"
  cat /tmp/ollama.log || true
  exit 1
fi

if ! ollama list | awk '{print $1}' | grep -qx "$AUTOREADME_MODEL"; then
  echo "Pulling default model: $AUTOREADME_MODEL"
  ollama pull "$AUTOREADME_MODEL"
fi

python3 -m app.main "$@"
