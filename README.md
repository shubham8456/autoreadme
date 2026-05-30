# AutoReadme

AutoReadme is a Docker-first README generator for local Git repositories. It mounts a repository from the host machine into a container, scans the project files, filters ignored content, sends the relevant context to Ollama, and writes the generated result to `README.generated.md` inside the mounted repository.

## Features

- Generate a README for a local Git repository using a single Docker command.
- Run Ollama inside the same container for a simple local setup.
- It skips noisy directories such as `.git`, `node_modules`, `dist`, and cache folders.
- Respect the repository's root `.gitignore` before sending files to the LLM.
- Persist Ollama models across runs using a Docker volume.
- Lets you override the default model at runtime with an environment variable.

## How it works

AutoReadme is designed around a mounted repository path.

1. A host repository is mounted into the container.
2. The container starts Ollama.
3. The Python app scans the mounted repository.
4. The scanner filters irrelevant files and ignored paths.
5. Selected project files are sent to the model through Ollama.
6. The generated README is written back to the mounted repository as `README.generated.md`.

## Run

```bash
docker run --rm \
  -v "$PWD:/workspace" \
  -v autoreadme_ollama:/root/.ollama \
  autoreadme /workspace
```
This uses the default model `qwen2.5-coder:3b` automatically.

<br>

Or, you can use any other model using env variable `-e AUTOREADME_MODEL=<your-model>`
```bash
docker run --rm \
  -e AUTOREADME_MODEL=llama3.2:3b \
  -v "$PWD:/workspace" \
  -v autoreadme_ollama:/root/.ollama \
  autoreadme /workspace
```
This downloads the model from [ollama](https://ollama.com/search) if not present in your machine already.
