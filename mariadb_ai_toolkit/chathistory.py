import mariadb
import json
from typing import List, Dict, Any

class ChatHistoryManager:
    """
    Manages and persists chat message history for an AI application using
    MariaDB's JSON data type for elegant state storage.

    This solves the tedious problem of maintaining conversation memory.
    """

    def __init__(self, connection_details: Dict[str, Any], table_name: str = "ai_chat_sessions"):
        self.connection_details = connection_details
        self.table_name = table_name
        self._ensure_table_exists()

    def _connect(self):
        """Establishes and returns a MariaDB connection."""
        try:
            return mariadb.connect(**self.connection_details)
        except mariadb.Error as e:
            print(f"MariaDB Connection Error: {e}")
            raise

    def _ensure_table_exists(self):
        """Creates the chat history table if it does not exist."""
        conn = self._connect()
        cursor = conn.cursor()
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                session_id VARCHAR(255) PRIMARY KEY,
                messages JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        try:
            cursor.execute(create_table_query)
            conn.commit()
            print(f"   -> Chat history table '{self.table_name}' is ready.")
        except mariadb.Error as e:
            print(f"MariaDB Schema Creation Error: {e}")
            raise
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()

    def add_message(self, session_id: str, role: str, content: str):
        """Adds a single message to a session's history, updating the JSON column."""
        conn = self._connect()
        cursor = conn.cursor()
        
        new_message = {"role": role, "content": content}
        
        try:
            # 1. Retrieve the existing messages
            select_query = f"SELECT messages FROM `{self.table_name}` WHERE session_id = ?"
            cursor.execute(select_query, (session_id,))
            result = cursor.fetchone()

            if result:
                # Session exists: append the new message
                messages = json.loads(result[0])
                messages.append(new_message)
                
                update_query = f"UPDATE `{self.table_name}` SET messages = ? WHERE session_id = ?"
                cursor.execute(update_query, (json.dumps(messages), session_id))
            else:
                # New session: create a new entry
                messages = [new_message]
                insert_query = f"INSERT INTO `{self.table_name}` (session_id, messages) VALUES (?, ?)"
                cursor.execute(insert_query, (session_id, json.dumps(messages)))
            
            conn.commit()
            print(f"   -> Saved message to session {session_id[:8]}...")
            
        except mariadb.Error as e:
            print(f"MariaDB Transaction Error: {e}")
            raise
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        """Retrieves the full chat history for a given session."""
        conn = self._connect()
        cursor = conn.cursor()
        
        try:
            select_query = f"SELECT messages FROM `{self.table_name}` WHERE session_id = ?"
            cursor.execute(select_query, (session_id,))
            result = cursor.fetchone()
        
            if result:
                return json.loads(result[0])
            else:
                return []
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()
