# ChatHistoryManager

## Overview
ChatHistoryManager provides persistent, scalable chat memory for AI applications using MariaDB's JSON type. It makes it easy to store and retrieve conversation history for any session.

## Why Chat Memory?
AI apps need memory to provide context-aware responses. Storing chat history in MariaDB's JSON column is fast, flexible, and scalable.

## Usage
```python
from mariadb_ai_toolkit.chathistory import ChatHistoryManager

chat_manager = ChatHistoryManager(connection_details=DB_CONNECTION_DETAILS)

session_id = "user123-session456"
chat_manager.add_message(session_id, "user", "Hello!")
chat_manager.add_message(session_id, "assistant", "Hi, how can I help?")

history = chat_manager.get_history(session_id)
for msg in history:
    print(msg["role"], msg["content"])
```

## How It Works
- **Table schema**: Stores each session's messages as a JSON array in a single row.
- **Add message**: Appends new messages to the session's history.
- **Get history**: Retrieves the full conversation for a session.

## Example Table Schema
```
session_id VARCHAR(255) PRIMARY KEY
messages JSON
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

## Advanced
- Supports multi-user, multi-session scenarios
- Can be extended for message types, timestamps, etc.
- Fast retrieval for long conversations

## Tips
- Use UUIDs for session IDs to avoid collisions.
- Secure sensitive chat data with proper database permissions.
