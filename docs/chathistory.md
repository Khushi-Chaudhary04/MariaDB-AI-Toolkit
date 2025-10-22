# 💬 ChatHistoryManager Documentation (Persistent Memory)

The `ChatHistoryManager` module (`mariadb_ai_toolkit.chathistory`) solves the fundamental challenge of providing AI applications with **reliable, persistent memory** in a production environment. It uses the flexible **MariaDB JSON** data type to store the complete conversation history for a session elegantly within a single database row.

---

## 💡 MariaDB Feature Showcase: JSON

This module is a direct demonstration of using MariaDB's `JSON` type for **flexible state management**.

* **Efficiency:** Storing the entire conversation as one JSON array is efficient for LLM context retrieval, as the entire history is often required in a single database read.
* **Simplicity:** It avoids complex relational models (many-to-one message tables) in favor of a clean, stateful design.

---

## 📝 Class: `ChatHistoryManager`

### Core Methods

| Method | Description |
| :--- | :--- |
| `__init__` | Ensures the `ai_chat_sessions` table (with the necessary `messages JSON` column) exists and establishes the database connection. |
| `add_message(session_id, role, content)` | **Appends a new message** to the session's history array in the `messages JSON` column. If the session is new, a row is created. |
| `get_history(session_id)` | **Retrieves the full conversation.** Returns the entire history as a native Python list of dictionaries, ready for the LLM context window. |

### Example Table Schema

The underlying table uses a clean, simple design for fast key-value retrieval:

```sql
CREATE TABLE IF NOT EXISTS `ai_chat_sessions` (
    session_id VARCHAR(255) PRIMARY KEY,
    messages JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
````

-----

## 💻 Usage Example

```python
from mariadb_ai_toolkit.chathistory import ChatHistoryManager
import uuid

# Initialize (DB_CONNECTION_DETAILS assumed to be available)
chat_manager = ChatHistoryManager(connection_details=DB_CONNECTION_DETAILS)

session_id = str(uuid.uuid4()) 
print(f"Starting new session: {session_id[:8]}...")

# 1. Add messages
chat_manager.add_message(session_id, "user", "I want to book a flight with United Airlines.")
chat_manager.add_message(session_id, "assistant", "I've filtered the routes for United. What is your destination?")

# 2. Retrieve the complete history
history = chat_manager.get_history(session_id)

# Output for LLM context
for msg in history:
    print(f"Role: {msg['role'].capitalize()} | Content: {msg['content']}")
````

**Expected Console Output:**

```
Starting new session: [unique-id]...
Role: User | Content: I want to book a flight with United Airlines.
Role: Assistant | Content: I've filtered the routes for United. What is your destination?
```
