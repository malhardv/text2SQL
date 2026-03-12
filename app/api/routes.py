from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import os
import shutil

from app.database.connection import get_db, engine
from app.database.schema_loader import get_database_schema
from app.llm.prompt_builder import build_sql_prompt
from app.llm.sql_generator import generate_sql
from app.services.sql_validator import validate_sql, InvalidQueryError
from app.services.query_executor import execute_query
from app.services.db_builder import build_database

router = APIRouter(prefix="/api")


class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    generated_sql: str
    columns: List[str]
    rows: List[Dict[str, Any]]

@router.post("/query", response_model=QueryResponse)
def process_natural_language_query(request: QueryRequest, db: Session = Depends(get_db)):
    try:
        # 1. Extract explicit database schema
        schema = get_database_schema()
        
        # 2. Construct prompt

        prompt = build_sql_prompt(schema, request.question)
        
        # 3. Send to LLM to generate SQL
        raw_sql = generate_sql(prompt)
        
        # 4. Validate SQL (Only SELECT allowed)
        validated_sql = validate_sql(raw_sql)
        
        # 5. Execute SQL
        query_results = execute_query(db, validated_sql)
        
        # 6. Return response
        return QueryResponse(
            question=request.question,
            generated_sql=validated_sql,
            columns=query_results["columns"],
            rows=query_results["rows"]
        )

    except InvalidQueryError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/setup")
async def setup_database(
    schema_file: UploadFile = File(...),
    csv_files: List[UploadFile] = File(...)
):
    """
    Accepts the .sql schema and multiple .csv data files,
    saves them temporarily, and rebuilds the sqlite database from scratch.
    """
    try:
        # Create an uploads directory
        uploads_dir = "uploads"
        os.makedirs(uploads_dir, exist_ok=True)
        
        # 1. Save Schema to the uploads dir so schema_loader.py finds it
        schema_path = os.path.join(uploads_dir, "schema.sql")
        with open(schema_path, "wb") as buffer:
            shutil.copyfileobj(schema_file.file, buffer)
            
        # 2. Save CSVs to the uploads directory
        csv_file_paths = []
        for csv in csv_files:
            if csv.filename.endswith(".csv"):
                path = os.path.join(uploads_dir, csv.filename)
                with open(path, "wb") as buffer:
                    shutil.copyfileobj(csv.file, buffer)
                csv_file_paths.append(path)
                
        # 3. Trigger DB Builder
        tables_created = build_database(csv_file_paths, schema_path, "test.db")
        
        # We can safely return success back to the React UI
        return {"message": "Setup successful", "tables_imported": tables_created}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to setup database: {str(e)}")

