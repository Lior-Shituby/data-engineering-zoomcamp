# Module 01 — Session 3
**Date: 2026-06-17**

## What Was Covered

### CLI Parameters with Click
- `click` library turns a Python script into a proper CLI tool
- `@click.command()` — marks the function as a CLI command
- `@click.option('--name', default=..., help=...)` — defines each CLI parameter with a default value
- Parameters are passed directly into the function as arguments
- Run with defaults: `uv run python ingest_data.py`
- Override a param: `uv run python ingest_data.py --month 2 --year 2021`
- Install: `uv add click`
- Click registers options with underscores (`--pg_user`), not hyphens — use `--help` to verify

### Docker Networking
- `docker network create pg-network` — create a named network for containers to communicate
- `--network=pg-network` — connect a container to that network
- `--name pgdatabase` — give a container a fixed name so others can reference it
- When containers are on the same network, use the container name as the host (e.g. `--pg_host=pgdatabase`), not `localhost`
- `docker rm <name>` — remove a stopped container (data in named volumes is safe)

### Running Ingest via Docker
```
docker run -it --rm `
  --network=pg-network `
  taxi_ingest:v001 `
  --pg_user=root `
  --pg_pass=root `
  --pg_host=pgdatabase `
  --pg_port=5432 `
  --pg_db=ny_taxi `
  --target_table=yellow_taxi_trips_2021_1 `
  --chunksize=100000
```

### Dockerfile Updates
- `COPY ingest_data.py .` and `ENTRYPOINT ["python", "ingest_data.py"]`
- Image tagged as `taxi_ingest:v001`
- `docker build --no-cache` needed when dependency changes aren't picked up from cache

## Previous Issue — RESOLVED (Session 4)
- Root cause: `ENV PATH="./code/.venv/bin:$PATH"` in Dockerfile used a relative path
- At runtime, WORKDIR is `/code`, so `./code/.venv/bin` resolved to `/code/code/.venv/bin` — nonexistent
- Python fell back to the system Python, which lacked `click`/`sqlalchemy`/`tqdm` → silent crash on import
- Fix: changed to `ENV PATH="/code/.venv/bin:$PATH"` (absolute path)

---

# Module 01 — Session 4
**Date: 2026-06-17 | Start: 12:45 | End: 14:30 | Duration: 1h 45m**

## What Was Covered

### Debugging the Silent Ingest Failure
- The Dockerfile had `ENV PATH="./code/.venv/bin:$PATH"` — a relative path
- Docker's `ENV` doesn't resolve relative to WORKDIR; at runtime `./code/.venv/bin` → `/code/code/.venv/bin` (doesn't exist)
- System Python ran instead of the venv Python — `import click` failed immediately, container exited silently
- Fix: `ENV PATH="/code/.venv/bin:$PATH"` — absolute path so the venv is always found
- Rebuilt with `docker build --no-cache -t taxi_ingest:v001 .`

### Successful Ingest Run
- `docker start pgdatabase` — restarted the existing stopped container (no data loss from named volume)
- Ran ingest via Docker against `pg-network`
- Result: 1,369,765 rows loaded into `yellow_taxi_trips`

### pgAdmin as Standalone Container
- `docker run ... --name pgadmin --network=pg-network dpage/pgadmin4`
- Access at `http://localhost:8085`, login with `admin@admin.com` / `root`
- Connect to Postgres using container name `pgdatabase` as the host (not `localhost`)

### Docker Compose
- `docker-compose.yaml` combines Postgres + pgAdmin into a single file
- `docker compose up` starts both services together
- Docker Compose auto-creates a network — no need to manually manage `pg-network`
- Services reach each other by service name (e.g. `pgdatabase`)
- Network name format: `<foldername>_default` — this project: `learningdataengineering_default`
- Volumes marked `external: true` to reuse existing named volumes (preserves data)
- Ingest container must join the Compose network: `--network=learningdataengineering_default`

## What's Next
- SQL refresher — join taxi trips with zone lookup table, run aggregation queries in pgAdmin
- Terraform / GCP setup
