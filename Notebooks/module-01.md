# Module 01 — Containerization & Infrastructure as Code

## What This Module Covers
- Ingesting NY taxi data into Postgres using Python
- Running Postgres + pgAdmin with Docker Compose
- Provisioning GCP infrastructure (GCS + BigQuery) with Terraform

---

## 1. Data Exploration (NY Taxi Dataset)

```python
import pandas as pd

prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'
url = f'{prefix}/yellow_tripdata_2021-01.csv.gz'

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]

df = pd.read_csv(url, dtype=dtype, parse_dates=parse_dates)
df.head()
```

---

## 2. Loading into Postgres

```python
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg://root:root@localhost:5432/ny_taxi')

# Create table schema
df.head(0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')

# Load in chunks
from tqdm.auto import tqdm

df_iter = pd.read_csv(url, dtype=dtype, parse_dates=parse_dates, iterator=True, chunksize=100000)

for df_chunk in tqdm(df_iter):
    df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')
```

---

## 3. Docker Setup

**docker-compose.yaml** runs:
- `pgdatabase` — Postgres (port 5432)
- `pgadmin` — pgAdmin UI (port 8080)

```bash
docker compose up -d
```

Access pgAdmin at `http://localhost:8080`

---

## 4. Ingest Pipeline

Located in `pipeline/` — runs as a Docker container, pulls NY taxi data and loads into Postgres.

```bash
cd pipeline
uv run ingest
```

---

## 5. GCP Infrastructure (Terraform)

Resources created in `terraform/`:
- **GCS bucket:** `de-zoomcamp-501007-data-lake` (data lake)
- **BigQuery dataset:** `ny_taxi` (data warehouse)

```bash
cd terraform
terraform init
terraform plan
terraform apply

# Tear down when done (safe wrapper)
.\destroy.ps1
```

**GCP Project:** `de-zoomcamp-501007` | Region: `us-central1`
