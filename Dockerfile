FROM ollama/ollama:latest

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml README.md ./
COPY app ./app
COPY docker/entrypoint.sh /entrypoint.sh

RUN pip3 install --no-cache-dir . \
    && chmod +x /entrypoint.sh

ENV OLLAMA_HOST=127.0.0.1:11434 \
    AUTOREADME_MODEL=qwen2.5-coder:3b \
    AUTOREADME_OUTPUT=README.generated.md \
    AUTOREADME_OLLAMA_URL=http://127.0.0.1:11434

ENTRYPOINT ["/entrypoint.sh"]
CMD ["."]
