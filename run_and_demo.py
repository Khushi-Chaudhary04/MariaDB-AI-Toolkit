import os
import uuid
from mariadb_ai_toolkit.ingestor import ingest_data_from_csv
from mariadb_ai_toolkit.vectorstore import HybridVectorStore
from mariadb_ai_toolkit.chathistory import ChatHistoryManager

# --- 1. DATABASE CONNECTION DETAILS ---
# This example assumes a local MariaDB instance with a database named 'mydb'.
DB_CONNECTION_DETAILS = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "root", # Replace with your MariaDB root password
    "database": "mydb"
}

# --- 2. FILE AND TABLE CONFIGURATION ---
CSV_FILE_PATH = "routes_demo.csv"
TABLE_NAME = "flight_routes"

def run_demo():
    """
    Executes a full demonstration of the MariaDB AI Toolkit:
    1. Ingests data with schema-aware mapping.
    2. Performs a hybrid vector search with metadata filtering.
    3. Manages chat history for a conversational AI.
    """
    print("--- MariaDB AI Toolkit Demonstration ---")

    # --- DEMO 1: SCHEMA-AWARE INGESTOR ---
    print("\n--- Part 1: Ingesting Flight Data ---")
    # Define which columns go to the embedding and which to metadata
    column_mapping = {
        "content": ["airline_name", "route_details"],
        "metadata": ["source_airport", "stops"]
    }
    ingest_data_from_csv(CSV_FILE_PATH, TABLE_NAME, DB_CONNECTION_DETAILS, column_mapping)

    # --- DEMO 2: HYBRID VECTOR STORE ---
    print("\n--- Part 2: Hybrid Search for Flight Routes ---")
    vector_store = HybridVectorStore(
        connection_details=DB_CONNECTION_DETAILS,
        table_name=TABLE_NAME
    )

    # Query for flights semantically similar to 'a quick flight to California'
    # BUT only include direct flights (stops=0) from United Airlines (airline='UA').
    query = "a quick flight to California"
    filters = {"stops": 0, "source_airport": "JFK"}
    
    print(f"\nSearching for: '{query}'")
    print(f"With filters: {filters}")

    search_results = vector_store.similarity_search(query=query, k=5, filter=filters)

    print("\n--- Top Search Results ---")
    if search_results:
        for doc in search_results:
            print(f"  - Text: {doc.page_content}")
            print(f"    Metadata: {doc.metadata}")
    else:
        print("No results found.")

    # --- DEMO 3: CHAT HISTORY MANAGER ---
    print("\n--- Part 3: Managing Chat History ---")
    session_id = str(uuid.uuid4())
    chat_manager = ChatHistoryManager(connection_details=DB_CONNECTION_DETAILS)

    print(f"\nStarting a new chat session: {session_id[:8]}...")
    chat_manager.add_message(session_id, "user", "Hi, I'm looking for flight information.")
    chat_manager.add_message(session_id, "assistant", "Of course! How can I help you today?")
    chat_manager.add_message(session_id, "user", "What was my first question?")

    history = chat_manager.get_history(session_id)
    print("\n--- Retrieved Chat History ---")
    for message in history:
        print(f"  - {message['role'].capitalize()}: {message['content']}")

    print("\n--- Demonstration Complete ---")

if __name__ == "__main__":
    # Check if the CSV file exists
    if not os.path.exists(CSV_FILE_PATH):
        print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
        print("Please make sure the CSV file is in the same directory as this script.")
    else:
        run_demo()
