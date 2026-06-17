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

## Current Issue — UNRESOLVED
- Ingest container ran but wrote 0 rows to Postgres
- `\dt` in pgcli shows empty database
- Container exited silently — need to scroll up in terminal for error output
- **Next session: debug why ingest_data.py failed silently inside Docker**

## What's Next
- Debug the silent ingest failure
- Continue with Docker Compose (running Postgres + pgAdmin together)
