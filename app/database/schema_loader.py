import os

# We will point this to wherever your .sql schema file lives
SCHEMA_FILE_PATH = "uploads/schema.sql"

def get_database_schema() -> str:
    """
    Reads the explicit schema directly from the user's .sql file
    and returns its text to be injected into the LLM prompt.
    """
    if os.path.exists(SCHEMA_FILE_PATH):
        with open(SCHEMA_FILE_PATH, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
            return f"Database Schema:\n{schema_sql}"
    
    # Fallback if no schema file found yet
    return "Error: Schema file not found. Ensure schema.sql exists."
