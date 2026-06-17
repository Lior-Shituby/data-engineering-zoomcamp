# Module 01 — Session 2 
**Date: 2026-06-16 | Start: 09:08 | End: 11:58 | Duration: 2h 50m**

## What Was Covered

### Dockerfile Evolution
- `COPY --from=<image>` — multi-stage trick to pull a binary (uv) directly from another Docker image into yours
- `COPY pyproject.toml .python-version uv.lock ./` — copy dependency files into the image
- **Order matters** — `COPY` must come *after* `WORKDIR` or files land in the wrong directory (root `/` instead of `/code`)
- `RUN uv sync --locked` — installs exact package versions from `uv.lock` inside the container (replaces `pip install`)
- `ENTRYPOINT ["python", "pipeline.py"]` with `ENV PATH="./code/.venv/bin:$PATH"` — cleaner than `uv run`, sets the venv Python as default
- `--no-cache` flag on build forces Docker to ignore cached layers: `docker build --no-cache -t test:pandas .`

### Key Docker Concepts
- `RUN pip install` vs `RUN uv sync --locked` — uv respects the lockfile, pip does not
- Docker caches layers aggressively — if a run fails unexpectedly after changes, rebuild with `--no-cache`
- `--rm` in `docker run` auto-deletes the container after it exits — remove it for databases so you can restart with `docker start <id>`
- `\` (Linux) vs `` ` `` (PowerShell) for multi-line commands in terminal

### Running PostgreSQL in Docker
```
docker run -it `
  -e POSTGRES_USER="root" `
  -e POSTGRES_PASSWORD="root" `
  -e POSTGRES_DB="ny_taxi" `
  -v ny_taxi_postgres_data:/var/lib/postgresql `
  -p 5432:5432 `
  postgres:17
```
- `-e` — sets environment variables inside the container (credentials, DB name)
- `-v named_volume:/path` — Docker-managed storage, data persists between container restarts
- `-p 5432:5432` — maps container port to your local machine's port
- `docker stop <id>` / `docker start <id>` — stop and restart without losing data
- Named volume keeps data safe even after container is deleted

### Connecting with pgcli
- `uv run pgcli -h localhost -p 5432 -u root -d ny_taxi` — connect to the running Postgres container
- `\dt` — list tables (backslash, not forward slash)
- Must be run from inside `pipeline/` folder where pgcli is installed

### Data Ingestion (ingest_data.py)
- `pd.read_csv(url, iterator=True, chunksize=100000)` — read large CSV in chunks
- `tqdm` — shows a progress bar while iterating
- `df.head(0).to_sql(..., if_exists='replace')` — create the table schema first
- `df_chunk.to_sql(..., if_exists='append')` — insert each chunk
- `uv add --dev jupyter` — install Jupyter as a dev-only dependency
- Iterator gets exhausted after one full loop — recreate `df_iter` to run again
- Notebook exploration code (like `df.head()`, `next(df_iter)`) doesn't belong in a script

### GitHub Setup
- Created public repo: https://github.com/Lior-Shituby/data-engineering-zoomcamp
- `git remote add origin <url>` — link local repo to GitHub
- `git push -u origin master` — first push, sets upstream tracking
- Authentication: used Personal Access Token (PAT) with `repo` scope
- If Git doesn't prompt for credentials, clear old ones from Windows Credential Manager

### Housekeeping Done
- Deleted stray `.venv` and `.venv-1` from project root
- Moved Dockerfile into `pipeline/` folder
- Restructured `ingest_data.py` — moved all logic inside `run()` function

## What's Next
- Verify `ingest_data.py` runs successfully end-to-end
- Continue with the Zoomcamp — Docker Compose for running Postgres + pgAdmin together
