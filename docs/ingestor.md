# 📂 Schema-Aware Ingestor Documentation: RAG Data Preparation

The `Schema-Aware Ingestor` module (`mariadb_ai_toolkit.ingestor`) is a powerful utility designed to automate the process of turning structured data (like CSVs) into the specific format required for **MariaDB Vector Search** and **Hybrid Search**. It effectively acts as a "RAG Data Pipeline in a Box."

---

## 💡 MariaDB Feature Showcase: Automated Indexing

The Ingestor abstracts away complex SQL DDL, providing two major benefits:

1.  **Unified Schema Creation:** It automatically creates the necessary columns for a hybrid approach: `text_data` (for source text), `metadata` (`JSON` type for filtering), and `embedding` (`VECTOR(384)` type for similarity).
2.  **Performance Guarantee:** It automatically adds the required high-performance **VECTOR INDEX** (`M=10 DISTANCE=COSINE`), ensuring that semantic search queries are fast and optimized from the moment data is ingested.

---

## 📝 Core Function: `ingest_data_from_csv()`

This function orchestrates the entire ingestion process in a single call.

```python
def ingest_data_from_csv(
    file_path: str,
    table_name: str,
    connection_details: Dict[str, Any],
    column_map: Dict[str, Union[str, List[str]]],
)
````

### Critical Parameter: `column_map`

This dictionary defines the **schema-awareness**, ensuring data integrity for RAG.

| Key | Value | Purpose |
| :--- | :--- | :--- |
| `"content"` | List of source column names | Columns that are concatenated to form the single text chunk used for **embedding generation**. |
| `"metadata"` | List of source column names | Columns whose values are serialized to the **MariaDB JSON** type for later **structured filtering**. |

### Usage Example

```python
from mariadb_ai_toolkit.ingestor import ingest_data_from_csv

column_map = {
    # 1. These fields define semantic meaning (used for HuggingFace embeddings)
    "content": ["airline_name", "route_details"], 
    
    # 2. These fields are for precision filtering (stored as JSON metadata)
    "metadata": ["source_airport", "stops"]
}

# DB_CONNECTION_DETAILS assumed to be available
ingest_data_from_csv(
    file_path="routes_demo.csv",
    table_name="flight_routes",
    connection_details=DB_CONNECTION_DETAILS,
    column_map=column_map
)
```

-----

## ⚙️ Ingestion Pipeline (The Five Steps)

1.  **Data Loading:** Loads the input CSV into a Pandas DataFrame.
2.  **Schema Preparation:** Executes a `DROP TABLE` and `CREATE TABLE` to set the necessary MariaDB schema, including `VECTOR(384)` and the `VECTOR INDEX`.
3.  **Text Combination:** Combines the columns specified in `"content"` into a single text field for each row.
4.  **Embedding Generation:** Generates vectors using the specified HuggingFace model.
5.  **Bulk Insertion:** Performs a single, efficient `cursor.executemany` operation to insert the text, the **JSON metadata string**, and the raw **vector bytes** into MariaDB.

### Example Table Schema (Automatically Generated)

```sql
id INT AUTO_INCREMENT PRIMARY KEY
text_data TEXT
metadata JSON
embedding VECTOR(384) NOT NULL
VECTOR INDEX vec_idx (embedding) M=10 DISTANCE=COSINE
```
