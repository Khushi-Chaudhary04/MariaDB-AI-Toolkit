# 🏆 MariaDB AI Toolkit: The Unified Python Bridge for AI/RAG

[![MariaDB Python Hackathon Submission](https://img.shields.io/badge/MariaDB%20Hackathon-Integration%20Track-blueviolet)](https://mariadb-python.hackerearth.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![LangChain Compatible](https://img.shields.io/badge/LangChain-Compatible-00a896)](https://www.langchain.com/)

The **MariaDB AI Toolkit** is a **production-ready Python package** that creates a **seamless developer experience** for building modern, context-aware AI applications. Submitted in the **Integration Track**, this toolkit directly exposes MariaDB's native capabilities (`VECTOR`, `JSON`) to the Python AI ecosystem, establishing MariaDB as a **unified data platform** for RAG.

---

## ✨ Features: Deeply Integrated RAG Components

This toolkit provides three core modules that automate the entire AI-data workflow:

### 1. Schema-Aware Ingestor
* **Automates Ingestion:** Handles structured data (CSV, DB tables) into MariaDB for vector search.
* **MariaDB Table Creation:** Automatically creates tables with **VECTOR** and **JSON** columns, and sets up a high-performance **VECTOR INDEX** (`M=10 DISTANCE=COSINE`).
* **Column Mapping:** Specify which columns are used for HuggingFace embeddings and which are stored as `JSON` metadata.

### 2. HybridVectorStore (LangChain Integration)
* **LangChain-Compatible:** A custom vector store built for the LangChain framework.
* **True Hybrid Search:** Combines semantic similarity (`VEC_DISTANCE_COSINE`) with structured JSON filtering (`JSON_VALUE`) in a **single, efficient query**.
* **Efficient Retrieval:** Leverages MariaDB's unified data platform for scalable, precise search.

### 3. ChatHistoryManager
* **Persistent Chat Memory:** Manages conversational state for AI applications using MariaDB's flexible **JSON** type.
* **Simple API:** Provides easy `add_message` and `get_history` functions for any session ID.
* **Fast and Flexible:** Ideal for scalable conversational AI and state management.

---

## 🛠️ Quickstart: Zero-Friction Setup

The included demonstration uses the **Open Flights Dataset** (or a derivative) to ensure the code's focus is on the features, not complex data setup.

1.  **Requirements:** Python 3.8+ and MariaDB Server (11.8+) with `VECTOR` and `JSON` support.
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure:** Update the `DB_CONNECTION_DETAILS` in `run_and_demo.py` with your credentials.
4.  **Run the Complete Demo:**
    ```bash
    python run_and_demo.py
    ```

### Demonstration Flow
* **Ingestor Demo:** Loads sample OpenFlights data, automatically creating the vector index.
* **Hybrid Search Demo:** Performs a query ranked by similarity *and* filtered by structured metadata.
* **Chat Manager Demo:** Simulates a chat session, persisting history to MariaDB.

---

## 📚 Project Structure & Documentation
```
mariadb-ai-toolkit/
├── mariadb_ai_toolkit/
│   ├── ingestor.py
│   ├── vectorstore.py
│   ├── chathistory.py
│   └── __init__.py
├── docs/
│   ├── ingestor.md
│   ├── vectorstore.md
│   └── chathistory.md
├── run_and_demo.py
├── requirements.txt
├── README.md
└── routes_demo.csv
```


