import os
import json

# Load messages from JSON
msg_file_path = os.path.join(os.path.dirname(__file__), "messages.json")
with open(msg_file_path, "r", encoding="utf-8") as f:
    TEXTS = json.load(f)

ERRORS = TEXTS["errors"]
MESSAGES = TEXTS["messages"]