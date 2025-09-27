import mariadb
import pandas as pd
import json
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
from typing import Dict, List, Any, Union

# --- CONFIGURATION CONSTANTS ---
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_EMBEDDING_DIM = 384 

def ingest_data_from_csv(
    file_path: str,
    table_name: str,
    connection_details: Dict[str, Any],
    column_map: Dict[str, Union[str, List[str]]],
):
    """
    Automates Schema-Aware data ingestion from a CSV into a MariaDB table.
    
    The function creates a table with VECTOR and JSON columns and handles:
    1. Loading and mapping data (combining 'content' for vector generation).
    2. Creating the necessary table schema with a VECTOR INDEX.
    3. Performing bulk insertion of text, metadata (JSON), and vectors.

    Args:
        file_path: Path to the CSV file.
        table_name: The name of the table to create/use in MariaDB.
        connection_details: Dictionary with MariaDB connection parameters.
        column_map: Defines which columns form the text content and which become JSON metadata.
            Example: {'content': ['col1', 'col2'], 'metadata': ['col3']}
    """
    print(f"--- Ingestor: Processing {file_path} into table '{table_name}' ---")
    
    conn = None
    try:
        conn = mariadb.connect(**connection_details)
        cursor = conn.cursor()

        # --- 1. Load Data ---
        df = pd.read_csv(file_path)
        print(f"   -> Loaded {len(df)} rows from CSV.")

        # --- 2. Prepare Schema and Embeddings ---
        embeddings_generator = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        
        # Create table with necessary VECTOR and JSON types
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS `{table_name}` (
                id INT AUTO_INCREMENT PRIMARY KEY,
                text_data TEXT,
                metadata JSON,
                embedding VECTOR({DEFAULT_EMBEDDING_DIM}) NOT NULL,
                -- Add VECTOR INDEX for high performance search (COSINE is standard for semantic search)
                VECTOR INDEX vec_idx (embedding) M=10 DISTANCE=COSINE
            );
        """
        cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`") # Drop for clean demo run
        cursor.execute(create_table_query)
        conn.commit()
        print(f"   -> Created table '{table_name}' with VECTOR and JSON columns.")

        # --- 3. Map Data and Generate Embeddings ---
        content_cols = column_map.get('content', [])
        metadata_cols = column_map.get('metadata', [])

        if not content_cols:
            raise ValueError("Column map must specify at least one column for 'content'.")

        # Create the combined text string for embedding
        texts = df[content_cols].apply(
            lambda x: " ".join([f"{col}: {x[col]}" for col in content_cols]), axis=1
        ).tolist()
        
        # Generate embeddings in bulk
        embeddings = embeddings_generator.embed_documents(texts)
        print(f"   -> Generated {len(embeddings)} vector embeddings using {EMBEDDING_MODEL_NAME}.")

        # Prepare bulk insert data
        insert_data = []
        for i, (text, embedding) in enumerate(zip(texts, embeddings)):
            # Create JSON metadata dictionary, ensuring values are JSON-serializable
            metadata_dict = {}
            for col in metadata_cols:
                if col in df.columns:
                    value = df.loc[i, col]
                    # Convert numpy types to native Python types
                    if hasattr(value, 'item'):
                        metadata_dict[col] = value.item()
                    else:
                        metadata_dict[col] = value
            # Convert embedding to bytes for MariaDB VECTOR column
            embedding_bytes = np.array(embedding, dtype='float32').tobytes()
            insert_data.append((
                text,
                json.dumps(metadata_dict),
                embedding_bytes
            ))

        # --- 4. Bulk Insert ---
        insert_query = f"INSERT INTO `{table_name}` (text_data, metadata, embedding) VALUES (?, ?, ?)"
        cursor.executemany(insert_query, insert_data)
        conn.commit()
        
        print(f"   -> Successfully ingested and vectorized {len(insert_data)} documents.")

    except mariadb.Error as e:
        print(f"MariaDB Error during ingestion: {e}")
        raise
    except ValueError as e:
        print(f"Ingestion Configuration Error: {e}")
        raise
    finally:
        if conn:
            cursor.close()
            conn.close()
