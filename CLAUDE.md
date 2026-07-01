# Claude Instructions — Data Engineering Zoomcamp

## About This Project

This is a **personal learning repo**, not a production codebase. The goal is to learn data engineering by following the [DataTalks.Club Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) curriculum. Explanations, notes, and structure should reflect that — prioritise understanding over polish.

## About the User

- Background: Industrial Engineering / Information Systems
- Current role: Data analyst (~1.8 years experience)
- Goal: Transition into data engineering
- Knows Python well — skip Python basics
- Frame new concepts (pipelines, orchestration, containers) in terms of analytical workflows and systems thinking, not from scratch

## Module Progress

| Module | Topic | Status |
|--------|-------|--------|
| 01 | Docker, Postgres, GCP, Terraform | Complete |
| 02 | Workflow orchestration with Kestra | In progress |
| 03+ | — | Not started |

**Module 01 built:**
- Local stack: Postgres 17 + pgAdmin in Docker
- Python ingest pipeline (`pipeline/`) — loads NY taxi CSV into Postgres
- GCP: GCS bucket + BigQuery dataset provisioned via Terraform
- Pre-commit hook blocking credential commits

**Module 02 goal:** Build ETL pipelines using Kestra (workflow orchestrator), load data into Postgres locally then GCS + BigQuery on GCP.

## Key Files

- `tui.py` — Interactive Terminal UI for all common commands. Run with `python tui.py` from project root.
- `docker-compose.yaml` — Local stack: Postgres (5432), pgAdmin (8085), Kestra (8080/8081)
- `pipeline/` — Python ingest pipeline (uv-managed, `uv run ingest` to execute)
- `terraform/` — GCP infrastructure as code
- `Notebooks/module-01.md` — Module 01 notes
- `Notebooks/module-02.md` — Module 02 notes and Kestra setup reference
- `Notes/` — Per-session notes and checklists

## Services & Ports

| Service  | URL / Port            | Credentials            |
|----------|-----------------------|------------------------|
| Kestra   | http://localhost:8080 | —                      |
| pgAdmin  | http://localhost:8085 | admin@admin.com / root |
| Postgres | localhost:5432        | root / root / ny_taxi  |

## GCP

- **Project ID:** `de-zoomcamp-501007`
- **Region:** `us-central1`
- **Bucket:** `de-zoomcamp-501007-data-lake`
- **BigQuery dataset:** `ny_taxi`
- **Credentials:** `~/.gcp/de-zoomcamp-credentials.json` (outside repo — never commit)
- `GOOGLE_APPLICATION_CREDENTIALS` is set as a persistent Windows env var

## GitHub

- Repo: https://github.com/Lior-Shituby/data-engineering-zoomcamp
- Default branch: `master`
