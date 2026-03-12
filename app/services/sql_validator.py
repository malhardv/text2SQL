import re

class InvalidQueryError(Exception):
    """Raised when the generated SQL query is not a safe SELECT statement."""
    pass

def validate_sql(query: str) -> str:
    """
    Ensures the query is a SELECT statement and blocks UPDATE, DELETE, INSERT, DROP, etc.
    Returns the query if valid, raises InvalidQueryError otherwise.
    """
    # 1. Strip reasoning blocks (like <think>...</think> from DeepSeek/Qwen models)
    query = re.sub(r"<think>.*?</think>", "", query, flags=re.IGNORECASE | re.DOTALL)
    
    # Also handle cases where only the closing tag is present (sometimes streaming APIs cut the start)
    if "</think>" in query:
        query = query.split("</think>")[-1]

    # 2. Try to extract SQL from markdown block if the LLM provided one
    # This handles formats like ```sql SELECT * FROM table ```
    match = re.search(r"```(?:sql)?\s+(.*?)\s+```", query, re.IGNORECASE | re.DOTALL)
    if match:
        query = match.group(1)
        
    # 3. Cleanup whitespace and loose ticks
    query = query.strip().strip("`").strip()
    
    # 3. Check if starts with SELECT (case-insensitive)
    if not re.match(r"^SELECT\s+", query, re.IGNORECASE):
        # Additional safety net: Sometimes models say "Here is the query: SELECT ..."
        # So we try to find the SELECT statement directly if we missed it.
        alt_match = re.search(r"(SELECT\s+.*)", query, re.IGNORECASE | re.DOTALL)
        if alt_match:
            query = alt_match.group(1)
        else:
            raise InvalidQueryError(f"Query must start with SELECT. Received: {query[:50]}...")
    # Check for forbidden keywords (very basic validation)
    forbidden_keywords = [r"\bUPDATE\b", r"\bDELETE\b", r"\bINSERT\b", r"\bDROP\b", r"\bALTER\b", r"\bTRUNCATE\b", r"\bGRANT\b", r"\bREVOKE\b"]
    for word in forbidden_keywords:
        if re.search(word, query, re.IGNORECASE):
            raise InvalidQueryError(f"Forbidden SQL command detected: {word.strip(r'\\b')}")
            
    return query
