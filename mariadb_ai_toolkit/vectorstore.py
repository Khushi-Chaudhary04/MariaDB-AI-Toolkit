import mariadb
import json
import numpy as np
from typing import Any, List, Optional, Dict, Union, Tuple

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain_core.embeddings import Embeddings
from langchain_huggingface import HuggingFaceEmbeddings

# --- CONFIGURATION CONSTANTS ---
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

class HybridVectorStore(VectorStore):
    """
    A custom LangChain VectorStore for MariaDB supporting advanced hybrid search.

    This class leverages MariaDB's native VECTOR and JSON types for
    combined semantic search and structured metadata filtering.
    """

    def __init__(
        self,
        connection_details: Dict[str, Any],
        table_name: str = "langchain_vectors",
        text_column: str = "text_data",
        metadata_column: str = "metadata",
        embedding_column: str = "embedding",
    ):
        """Initializes the HybridVectorStore."""
        self.connection_details = connection_details
        self.table_name = table_name
        self.text_column = text_column
        self.metadata_column = metadata_column
        self.embedding_column = embedding_column
        
        # Use the standard HuggingFace embedding model for consistency
        self.embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    def _connect(self):
        """Establishes and returns a MariaDB connection."""
        try:
            return mariadb.connect(**self.connection_details)
        except mariadb.Error as e:
            print(f"MariaDB Connection Error: {e}")
            raise

    @property
    def embeddings(self) -> Embeddings:
        """Returns the embedding model instance."""
        return self.embedding_model

    # NOTE: add_documents and _delete methods are omitted here to focus on the
    # core features (Ingestor and Hybrid Search), but would be required
    # for a fully compliant LangChain VectorStore implementation.

    @classmethod
    def from_texts(cls, texts: List[str], embedding: Embeddings, metadatas: Optional[List[dict]] = None, **kwargs: Any):
        """
        Required by LangChain VectorStore interface. Not used in this MariaDB toolkit implementation.
        """
        raise NotImplementedError("Use the Ingestor for bulk loading. HybridVectorStore is for search only.")

    def similarity_search(
        self, query: str, k: int = 4, filter: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> List[Document]:
        """
        Performs the Hybrid Vector Search with optional metadata filtering.

        Combines VEC_DISTANCE_COSINE for semantic search with structured JSON filtering.
        """
        conn = self._connect()
        cursor = conn.cursor()

        # 1. Generate the embedding for the query string
        query_embedding = self.embedding_model.embed_query(query)
        # Convert query embedding to bytes for MariaDB VECTOR comparison
        query_embedding_bytes = np.array(query_embedding, dtype='float32').tobytes()

        # 2. Build the dynamic SQL query
        sql_query_base = f"SELECT {self.text_column}, {self.metadata_column} FROM `{self.table_name}`"
        where_clauses: List[str] = []
        params: List[Any] = []

        # Process structured metadata filters (JSON filtering)
        if filter:
            for key, value in filter.items():
                # Uses JSON_VALUE to query the JSON column efficiently
                where_clauses.append(f"JSON_VALUE({self.metadata_column}, '$.{key}') = ?")
                params.append(str(value)) 

        # Construct WHERE clause
        if where_clauses:
            sql_query_base += " WHERE " + " AND ".join(where_clauses)
        
        # 3. Add Vector Distance Sorting and Limit
        # The key elegant implementation: VEC_DISTANCE on the vector column
        sql_query = sql_query_base + f"""
            ORDER BY VEC_DISTANCE_COSINE({self.embedding_column}, ?)
            LIMIT ?;
        """
        params.extend([query_embedding_bytes, k])

        try:
            cursor.execute(sql_query, tuple(params))
            results = cursor.fetchall()
            
            # 4. Convert results back to LangChain Documents
            documents = []
            for text, metadata_json in results:
                documents.append(
                    Document(
                        page_content=text,
                        metadata=json.loads(metadata_json) if metadata_json else {},
                    )
                )
            
            print(f"   -> Found {len(documents)} relevant documents.")
            return documents

        except mariadb.Error as e:
            print(f"MariaDB Search Error: {e}")
            raise
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()
    
    # Required method stub
    def add_texts(self, texts: List[str], metadatas: Optional[List[dict]] = None, **kwargs: Any) -> List[str]:
         raise NotImplementedError("This method is designed for the Ingestor tool. Use Ingestor for bulk loading.")
    
    # Required method stub
    def _delete(self, ids: Optional[List[str]] = None, **kwargs: Any) -> Optional[bool]:
        raise NotImplementedError("Delete method is not implemented for this toolkit version.")
