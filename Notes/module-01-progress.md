# Module 01 — Docker & Environment Setup
**Date: 2026-06-15**

## Docker Basics
- **Image** = template (e.g. `python:3.12`). **Container** = a running instance of that image
- Containers are isolated and stateless — changes inside don't persist after they stop
- `docker run -it <image>` — start a container and attach your terminal
- `--entrypoint=bash` — opens a bash shell instead of the image's default program
- `-v "$(pwd):/app"` — mounts your local folder into the container so it can access your files

## Python Environment Management with uv
- Installing packages globally causes version conflicts across projects
- Virtual environments isolate dependencies per project
- `uv add <package>` installs into the project's `.venv` only, not system Python
- `uv run python` uses the isolated environment — not your system Python 3.14
- VS Code interpreter should point to `.venv\Scripts\python.exe`

## Data Pipeline Concept
- A pipeline takes data in (CSV) and produces outputs — Parquet file, PostgreSQL, Data Warehouse
- `sys.argv` lets you pass arguments to a Python script from the terminal (e.g. `python pipeline.py 10`)

## Git Basics
- `git init` — initialize a new git repository in the current folder
- `git status` — show what files have changed, what's staged, what's untracked
- `git add .` — stage all changed files in the current directory for commit
- `git commit -m "message"` — save a snapshot of staged files with a label
- A commit is a checkpoint — you can roll back to it if something breaks
- LF/CRLF warnings on Windows are harmless — just Git converting line endings

## Dockerfile Basics
- A Dockerfile defines how to build a Docker image for your project
- `FROM <image>` — base image to start from
- `RUN <command>` — execute a command during the build (e.g. install packages)
- `WORKDIR <path>` — set the working directory inside the container
- `COPY <src> <dest>` — copy files from your machine into the image
- `ENTRYPOINT ["python", "pipeline.py"]` — the command that runs when the container starts
- Build with: `docker build -t <name>:<tag> .` — the `.` means use the current folder
- The `-t` in `docker build` means **tag** (name the image), not terminal
- `--rm` in `docker run` — auto-delete the container after it exits
- Always rebuild after changing the Dockerfile — Docker caches old layers
- Keep the Dockerfile in the same folder as the files it references

## Terminal — Windows vs Linux
- Teacher uses Linux/Mac — some commands won't work in PowerShell
- `touch` → `New-Item`
- `which python` → `uv run python -c "import sys; print(sys.executable)"`
- `ls` works in PowerShell too
- Inside a Docker container you're on Linux, so course commands work there
