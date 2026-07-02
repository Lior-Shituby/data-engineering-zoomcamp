# Data Engineering Zoomcamp — Learning Repo

Personal learning repo following the [DataTalks.Club Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp).

## Module Progress

| Module | Topic | Status |
|--------|-------|--------|
| 01 | Docker, Postgres, GCP, Terraform | Complete |
| 02 | Workflow orchestration with Kestra | In progress |
| 03+ | — | Not started |

## Project Structure

```
.
├── docker-compose.yaml              # Full local stack: Postgres, pgAdmin, Kestra + its Postgres
├── pgadmin-servers.json             # pgAdmin server config (auto-loaded by compose)
├── tui.py                           # Terminal UI — interactive menu for all common commands
├── CLAUDE.md                        # AI assistant context for this project
├── Notebook.md                      # Early data exploration (Jupyter notebook export)
├── data-engineering-zoomcamps-doco  # Course documentation reference
├── de-zoomcamp.code-workspace       # VS Code workspace
│
├── pipeline/                        # Python ingest pipeline (uv-managed)
│   ├── pyproject.toml
│   ├── uv.lock
│   └── ingest_data.py
│
├── terraform/                       # GCP infrastructure (IaC)
│   ├── main.tf                      # GCS data lake bucket + BigQuery dataset
│   ├── variables.tf
│   ├── outputs.tf
│   └── destroy.ps1                  # Safe destroy wrapper (preview + confirm)
│
├── Notebooks/                       # Module notes
│   ├── module-01.md
│   └── module-02.md
│
├── Notes/                           # Session notes and checklists
│   ├── module-01-progress.md
│   ├── module-01-session-*.md
│   ├── gcp-setup-checklist.md
│   └── security-review.md
│
└── test/                            # Scratch/test files
```

## Services & Ports

| Service         | URL / Port            | Credentials                        |
|-----------------|-----------------------|------------------------------------|
| Kestra UI       | http://localhost:8080 | admin@kestra.io / Admin1234!       |
| pgAdmin         | http://localhost:8085 | admin@admin.com / root             |
| Postgres (taxi) | localhost:5432        | root / root / ny_taxi              |
| Postgres (kestra)| internal only        | kestra / k3str4 / kestra           |

## Quick Start

```powershell
# Start full local stack (Postgres, pgAdmin, Kestra)
docker compose up -d

# Open Kestra UI
# http://localhost:8080  →  admin@kestra.io / Admin1234!

# Run ingest pipeline
cd pipeline
uv run ingest

# Or use the interactive TUI for everything
python tui.py
```

## GCP

```powershell
# Provision GCP infrastructure
cd terraform
terraform init
terraform plan
terraform apply

# Tear down safely (shows preview + requires typing 'destroy')
.\destroy.ps1
```

## GCP Project

- **Project ID:** `de-zoomcamp-501007`
- **Project Number:** `347194603655`
- **Region:** `us-central1`
- **Resources:** GCS bucket (`de-zoomcamp-501007-data-lake`), BigQuery dataset (`ny_taxi`)

## Credentials & Secrets

- Service account key: `~/.gcp/de-zoomcamp-credentials.json` (outside repo, never committed)
- DB credentials: `.env` (gitignored)
- Pre-commit hook blocks accidental credential commits
