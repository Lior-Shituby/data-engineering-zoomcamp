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

## Terminal — Windows vs Linux
- Teacher uses Linux/Mac — some commands won't work in PowerShell
- `touch` → `New-Item`
- `which python` → `uv run python -c "import sys; print(sys.executable)"`
- `ls` works in PowerShell too
- Inside a Docker container you're on Linux, so course commands work there
