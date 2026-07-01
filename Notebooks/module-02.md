# Module 02 — Workflow Orchestration with Kestra

## What This Module Covers
- Workflow orchestration fundamentals
- Kestra core concepts: flows, tasks, triggers
- ETL pipelines: NY taxi data → Postgres
- Scheduling and backfilling
- Cloud deployment: GCS + BigQuery
- AI integration (Copilot + RAG)
- Production deployment and Git sync

---

## Prerequisites Checklist
- [X] Module 01 complete
- [X] Docker + Docker Compose installed
- [X] GCP account with GCS bucket + BigQuery dataset provisioned
- [ ] Gemini API key (from https://aistudio.google.com) — needed for AI sections

---

## Setup — Running Kestra with Docker

Kestra is added to the existing `docker-compose.yaml` alongside Postgres and pgAdmin so all services share the same Docker network (needed for Kestra to write data into Postgres).

The Kestra service block added to `docker-compose.yaml`:

```yaml
kestra:
  image: kestra/kestra:latest
  pull_policy: always
  entrypoint: /bin/bash
  command: -c 'export KESTRA_CONFIGURATION_SECRET=$(echo -n "mysecret" | base64) && /app/kestra server standalone'
  volumes:
    - kestra-data:/app/storage
    - /var/run/docker.sock:/var/run/docker.sock  # lets Kestra spawn Docker containers for worker tasks
  ports:
    - "8080:8080"   # Kestra UI
    - "8081:8081"   # Kestra management API
  depends_on:
    - pgdatabase
```

Notes:
- Standalone mode uses an embedded H2 database — fine for local dev
- `KESTRA_CONFIGURATION_SECRET` is used to encrypt secrets stored in Kestra
- `/var/run/docker.sock` is exposed by Docker Desktop on Windows via WSL2

### Docker Compose Commands

```bash
# Start all services (Postgres, pgAdmin, Kestra)
docker compose up -d

# Start only Kestra (if Postgres is already running)
docker compose up -d kestra

# Check which services are running and their ports
docker compose ps

# Stream Kestra logs live
docker compose logs -f kestra

# Stop all containers (data is preserved in volumes)
docker compose down

# Stop and wipe all volumes — resets all data (destructive)
docker compose down -v
```

Access:
- **Kestra UI** → http://localhost:8080
- **pgAdmin** → http://localhost:8085
- **Postgres** → `localhost:5432` (user: `root`, pass: `root`, db: `ny_taxi`)

---

## Key Concepts

### Flow
A workflow definition in YAML — the basic unit of work in Kestra.

```yaml
id: my_first_flow
namespace: dev

tasks:
  - id: hello
    type: io.kestra.plugin.core.log.Log
    message: "Hello from Kestra!"
```

### Task
A single step inside a flow (e.g. run a Python script, query a database, upload a file).

### Trigger
What kicks off a flow — a schedule, a webhook, another flow finishing, etc.

### Namespace
Logical grouping for flows (like a folder). E.g. `zoomcamp.module02`.

---

## ETL Pipeline — NY Taxi → Postgres

*(Fill in as you work through the module)*

```python
# Notes go here
```

---

## Scheduling & Backfilling

*(Fill in as you work through the module)*

---

## GCP Integration (GCS + BigQuery)

Resources already provisioned from Module 01:
- Bucket: `de-zoomcamp-501007-data-lake`
- Dataset: `ny_taxi`

*(Fill in Kestra flows for GCS/BigQuery as you work through the module)*

---

## Notes & Observations

*(Add notes here as you progress)*
