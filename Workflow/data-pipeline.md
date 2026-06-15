# Data Pipeline Workflow

```mermaid
flowchart LR
    A[CSV File] --> B[Data Pipeline]
    B --> C[Parquet File]
    B --> D[PostgreSQL Database]
    B --> E[Data Warehouse]

    style B fill:#4CAF50,color:#fff
```
