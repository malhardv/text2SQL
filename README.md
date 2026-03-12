# Text-to-SQL AI System

A production-style backend system that converts natural language questions into SQL queries, executes them on a relational database, and returns the results. 

Built with:
- **Python** (>=3.10)
- **uv** (Dependency Management)
- **FastAPI** (Web Framework)
- **SQLAlchemy** (Database Access & Introspection)
- **Groq API** (LLM inference)

## Prerequisites
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed on your machine.
- A [Groq API Key](https://console.groq.com/keys).

## Setup Instructions

### 1. Install uv
If you haven't already installed `uv`, you can do so by running:
```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Create Virtual Environment & Install Dependencies
Navigate to the project directory and run:

```bash
uv venv
# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies from pyproject.toml
uv pip install -e .
```

### 3. Configure Environment Variables
Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```
Edit the `.env` file and add your `GROQ_API_KEY`. By default, it uses a local SQLite database for testing, but you can change `DATABASE_URL` to a PostgreSQL connection string.

### 4. Run the FastAPI Server
Start the backend server using Uvicorn:

```bash
uvicorn app.main:app --reload
```
The server will start at `http://127.0.0.1:8000`.

### 5. Test the API Endpoint
You can test the `/query` endpoint using `curl` or by visiting the interactive Swagger UI documentation at `http://127.0.0.1:8000/docs`.

**Example cURL Request:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/query' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "Show me all users."
}'
```
