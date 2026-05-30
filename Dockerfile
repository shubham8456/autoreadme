FROM alpine/ollama:latest

RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-virtualenv \
    ca-certificates \
    curl \
    && ln -sf python3 /usr/bin/python

WORKDIR /app

COPY pyproject.toml ./
COPY app ./app
COPY docker/entrypoint.sh /entrypoint.sh

RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir --no-compile . \
    && chmod +x /entrypoint.sh

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    AUTOREADME_MODEL=qwen2.5-coder:3b \
    AUTOREADME_OLLAMA_URL=http://127.0.0.1:11434

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/workspace"]
