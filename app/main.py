from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.api.routes import router

app = FastAPI(title="Text-to-SQL API", version="0.1.0")

# Use Environment variable for production Vercel URL, else fallback to open CORS
allowed_origins = os.getenv("FRONTEND_URL", "*").split(",")

# Allow the React frontend properly connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Text-to-SQL API. Visit /docs to test the API."}
