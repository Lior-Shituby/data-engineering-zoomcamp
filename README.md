# Data Engineering Zoomcamp — Learning Repo

Personal learning repo following the [DataTalks.Club Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp).

## Project Structure

```
.
├── docker-compose.yaml              # Postgres + pgAdmin local stack
├── pgadmin-servers.json             # pgAdmin server config (auto-loaded by compose)
├── tui.py                           # Terminal UI for running pipeline commands interactively
├── Notebook.md                      # Early data exploration (Jupyter notebook export)
├── data-engineering-zoomcamps-doco  # Course documentation reference
├── de-zoomcamp.code-workspace       # VS Code workspace (open this for organized explorer)
│
├── pipeline/                        # Python ingest pipeline
│   ├── pyproject.toml               # Dependencies (uv)
│   ├── uv.lock                      # Locked dependency versions
│   └── .venv/                       # Virtual environment (gitignored)
│
├── terraform/                       # GCP infrastructure (IaC)
│   ├── main.tf                      # GCS data lake bucket + BigQuery dataset
│   ├── variables.tf                 # Project ID, region
│   ├── outputs.tf                   # Outputs printed after apply
│   └── destroy.ps1                  # Safe destroy wrapper (preview + confirm)
│
├── Notes/                           # Session notes and checklists
│   ├── module-01-progress.md        # Module 01 progress tracker
│   ├── module-01-session-*.md       # Per-session notes
│   ├── gcp-setup-checklist.md       # GCP + Terraform setup steps
│   └── security-review.md          # Security notes
│
├── Workflow/                        # Reference docs
│   └── data-pipeline.md            # Pipeline architecture notes
│
└── test/                            # Scratch/test files
```

## Credentials & Secrets

- Service account key: `~/.gcp/de-zoomcamp-credentials.json` (outside repo, never committed)
- DB credentials: `.env` (gitignored)
- Pre-commit hook blocks accidental credential commits

## Quick Start

```powershell
# Start local Postgres + pgAdmin
docker compose up -d

# Run ingest pipeline
cd pipeline
uv run ingest

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
