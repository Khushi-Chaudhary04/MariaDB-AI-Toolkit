# MariaDB AI Toolkit

A production-ready Python package featuring three deeply integrated modules that automate the entire AI-data workflow for Retrieval-Augmented Generation (RAG) and hybrid search applications using MariaDB.

## Features

### 1. Schema-Aware Ingestor
- **Automates ingestion** of structured data (CSV, database tables) into MariaDB for vector search.
- **Column mapping:** Specify which columns are used for embeddings and which are stored as JSON metadata.
- **Embeddings:** Uses HuggingFace models for semantic vector generation.
- **MariaDB Table Creation:** Automatically creates tables with VECTOR and JSON columns, and a VECTOR INDEX for fast search.

### 2. HybridVectorStore
- **LangChain-compatible** vector store for MariaDB.
- **Hybrid search:** Combines semantic similarity (VEC_DISTANCE_COSINE) with structured JSON filtering in a single query.
- **Efficient retrieval:** Leverages MariaDB's unified data platform for scalable, precise search.

### 3. ChatHistoryManager
- **Persistent chat memory** for AI applications using MariaDB's JSON type.
- **Simple API:** Add and retrieve chat messages for any session.
- **Fast and flexible:** Ideal for conversational AI and state management.

## Quickstart

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure your MariaDB connection** in `run_and_demo.py`:
   ```python
   DB_CONNECTION_DETAILS = {
       "host": "127.0.0.1",
       "port": 3306,
       "user": "root",
       "password": "your_password",
       "database": "mydb"
   }
   ```
3. **Run the demonstration:**
   ```bash
   python run_and_demo.py
   ```

## Demonstration

- **Ingestor Demo:** Loads a sample OpenFlights CSV, mapping columns for embeddings and metadata.
- **Hybrid Search Demo:** Finds routes similar to a query, filtered by airline and stops.
- **Chat Manager Demo:** Simulates a chat session and retrieves the history.

## Project Structure
```
mariadb-ai-toolkit/
├── mariadb_ai_toolkit/
│   ├── ingestor.py
│   ├── vectorstore.py
│   ├── chathistory.py
│   └── __init__.py
├── run_and_demo.py
├── requirements.txt
├── README.md
└── routes_demo.csv
```

## Requirements
- Python 3.8+
- MariaDB server (with VECTOR and JSON support)
- See `requirements.txt` for Python dependencies

## License
MIT
