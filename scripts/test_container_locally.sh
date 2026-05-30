#!/bin/sh

# TEST_REPO_PATH="/Users/user_1/dev/path/to/repo/root"

# Step 1: `docker build -t autoreadme-alpine-dev`
# Step 2:
docker run --rm -it \
  --entrypoint sh \
  -v "$PWD:/app" \
  -v "$TEST_REPO_PATH:/workspace" \
  -v autoreadme_ollama:/root/.ollama \
  -w /app \
  autoreadme-alpine-dev \
  -c 'ollama serve >/tmp/ollama.log 2>&1 & \
      until curl -fsS http://127.0.0.1:11434/api/tags >/dev/null; do sleep 1; done; \
      pip install -e . && \
      python -m app.main /workspace'
