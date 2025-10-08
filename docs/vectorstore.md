# HybridVectorStore

## Overview
HybridVectorStore is a LangChain-compatible vector store for MariaDB that enables true hybrid search: combining semantic similarity (vector search) and structured filtering (JSON) in a single query.

## Why Hybrid Search?
Most systems only support either semantic search or structured filtering. HybridVectorStore lets you do both, so you can run queries like "find routes similar to X, but only direct flights from airline Y."

## Usage
```python
from mariadb_ai_toolkit.vectorstore import HybridVectorStore

vector_store = HybridVectorStore(
    connection_details=DB_CONNECTION_DETAILS,
    table_name="flight_routes"
)

results = vector_store.similarity_search(
    query="a quick flight to California",
    k=5,
    filter={"stops": 0, "source_airport": "JFK"}
)
```

## How It Works
- **Semantic search**: Uses VEC_DISTANCE_COSINE on the VECTOR column for similarity.
- **Structured filtering**: Uses JSON_VALUE on the metadata column for precise filtering.
- **Single query**: Combines both in one SQL statement for speed and accuracy.

## Example Query
```
SELECT text_data, metadata
FROM flight_routes
WHERE JSON_VALUE(metadata, '$.stops') = 0 AND JSON_VALUE(metadata, '$.source_airport') = 'JFK'
ORDER BY VEC_DISTANCE_COSINE(embedding, <query_vector>)
LIMIT 5;
```

## Advanced
- Fully compatible with LangChain for RAG and AI workflows
- Customizable for other metadata fields and embedding models
- Scalable for large datasets

## Tips
- Use hybrid search to combine semantic relevance with business logic filters.
- Tune VECTOR INDEX parameters for optimal performance.
