def build_sql_prompt(schema: str, question: str) -> str:
    """
    Constructs the prompt including database schema and instructions.
    """
    prompt = f"""You are a helpful SQL assistant. Your job is to convert the given natural language question into a valid SQL SELECT query. 
    
DO NOT wrap the SQL in markdown tags (like ```sql).
ONLY return the SQL query string. 
DO NOT include any conversational text like "Here is the query".
Ensure the query ONLY uses the tables and columns provided in the schema below.

{schema}

User Question: {question}

SQL Query:"""
    return prompt.strip()
