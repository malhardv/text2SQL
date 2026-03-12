from sqlalchemy.orm import Session
from sqlalchemy import text

def execute_query(db: Session, query: str):
    """
    Executes a validated SQL query and returns the column names and result rows.
    """
    result = db.execute(text(query))
    columns = list(result.keys())
    # fetchall() returns Row objects. We can map them directly into dictionaries or return them directly.
    # To return a list of lists/tuples as requested, or list of dicts:
    rows = [dict(zip(columns, row)) for row in result.fetchall()]
    
    return {"columns": columns, "rows": rows}
