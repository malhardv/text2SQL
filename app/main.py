from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(title="Text-to-SQL API", version="0.1.0")

# Allow the React frontend properly connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For simplicity in local dev. Use ["http://localhost:5173"] in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Text-to-SQL API. Visit /docs to test the API."}
