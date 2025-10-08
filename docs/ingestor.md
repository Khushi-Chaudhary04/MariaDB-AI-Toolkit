# Schema-Aware Ingestor

## Overview
The Ingestor module automates the process of transforming structured data (CSV, database tables) into the format required for vector search in MariaDB. It is schema-aware, allowing you to specify which columns are used for semantic embeddings and which are stored as JSON metadata for precise filtering.

## Why Schema-Awareness Matters
Traditional ingestion tools combine all columns into a single text field, losing the ability to filter or retrieve by structured metadata. The Ingestor solves this by letting you map columns for embeddings and metadata separately, ensuring both semantic and structured accuracy.

## Usage
```python
from mariadb_ai_toolkit.ingestor import ingest_data_from_csv

column_map = {
    "content": ["airline_name", "route_details"],
    "metadata": ["source_airport", "stops"]
}

ingest_data_from_csv(
    file_path="routes_demo.csv",
    table_name="flight_routes",
    connection_details=DB_CONNECTION_DETAILS,
    column_map=column_map
)
```

## How It Works
1. **Loads CSV data** into a Pandas DataFrame.
2. **Maps columns**: Combines specified columns into a text field for embeddings, others into JSON metadata.
3. **Generates embeddings** using HuggingFace models.
4. **Creates MariaDB table** with VECTOR and JSON columns, and a VECTOR INDEX.
5. **Bulk inserts** data, ensuring all vectors and metadata are correctly formatted.

## Advanced
- Supports other structured sources (database tables, etc.)
- Handles large datasets efficiently
- Robust error handling for schema and data issues

## Example Table Schema
```
id INT AUTO_INCREMENT PRIMARY KEY
text_data TEXT
metadata JSON
embedding VECTOR(384) NOT NULL
VECTOR INDEX vec_idx (embedding) M=10 DISTANCE=COSINE
```

## Tips
- Use schema-awareness to optimize both semantic and structured retrieval.
- For very large datasets, consider batching inserts.
