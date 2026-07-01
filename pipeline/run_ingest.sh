# Reference: manual docker run commands used during Module 01 debugging

# Start Postgres standalone (before Docker Compose was set up)
docker run -it `
  -e POSTGRES_USER="root" `
  -e POSTGRES_PASSWORD="root" `
  -e POSTGRES_DB="ny_taxi" `
  -v ny_taxi_postgres_data:/var/lib/postgresql `
  -p 5432:5432 `
  --network=pg-network `
  --name pgdatabase `
  postgres:17

# Run ingest container against Postgres
docker run -it --rm \
  --network=pg-network \
  taxi_ingest:v001 \
  --pg_user=root \
  --pg_pass=root \
  --pg_host=pgdatabase \
  --pg_port=5432 \
  --pg_db=ny_taxi \
  --target_table=yellow_taxi_trips
