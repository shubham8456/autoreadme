FROM ollama/ollama:latest

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       python3 python3-pip python3-venv \
       ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml README.md ./
COPY app ./app
COPY docker/entrypoint.sh /entrypoint.sh

RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir . \
    && chmod +x /entrypoint.sh

ENV PATH="/opt/venv/bin:$PATH"
ENV AUTOREADME_MODEL=qwen2.5-coder:3b \
    AUTOREADME_OLLAMA_URL=http://127.0.0.1:11434

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/workspace"]
