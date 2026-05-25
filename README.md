## autoreadme

Generate README files for local git repositories using a Docker container with Ollama running inside it.

### Run

```bash
docker run --rm \
  -v "$PWD:/workspace" \
  autoreadme .
```

```bash
docker run --rm \
  -v "$PWD:/workspace" \
  -v autoreadme_ollama:/root/.ollama \
  autoreadme /workspace
```

The container analyzes the mounted repository and writes README.generated.md to the mounted directory.


### Architecture

- A single Docker image contains both Ollama and the Python application.
- Container startup launches Ollama, ensures a default model is present, then runs the app.
- The app scans a mounted repository, builds a prompt, asks Ollama to generate markdown, and writes `README.generated.md`.
