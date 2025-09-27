# Expose the core components for easy import (e.g., from mariadb_ai_toolkit import Ingestor)
from .ingestor import ingest_data_from_csv
from .vectorstore import HybridVectorStore
from .chathistory import ChatHistoryManager

# Define the package version
__version__ = "0.1.0"
