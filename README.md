# Text-to-SQL AI System

A full-stack, production-ready application that securely converts natural language questions into executable SQL queries, runs them against a database, and returns the live data in a sleek React user interface.

It features a 2-step process where users can upload a `.sql` schema and multiple `.csv` data files to dynamically initialize a fresh SQLite database entirely through the browser before querying.

## 🚀 Tech Stack

**Backend (Python API)**
- **FastAPI**: High-performance REST API handling the core orchestration.
- **SQLAlchemy**: Safely interacts with the database and fetches the data.
- **Groq API**: Blazing fast LLM inference (using `qwen-2.5-32b`).
- **uv**: Modern, incredibly fast Python dependency management.

**Frontend (React)**
- **Vite & React**: Lightning-fast frontend tooling and component architecture.
- **Lucide React**: Beautiful, consistent iconography.
- **Vanilla CSS**: Custom-tailored dark mode, glassmorphism UI with micro-animations.

---

## 🛠️ Complete Project Workflow

1. **Initialization Flow**:
   - The user opens the React app and is presented with a Setup Screen.
   - They drag-and-drop a `schema.sql` file and any number of `.csv` files.
   - The React app sends these files to the FastAPI `/api/setup` endpoint.
   - The backend deletes any old `test.db`, executes the `schema.sql` to build the table structures perfectly, and then leverages `pandas` to insert all the CSV data into those tables.
   
2. **Text-to-SQL Flow**:
   - The user types a natural language question in the Chat UI.
   - The server routes request to `/api/query`.
   - `schema_loader.py` dynamically reads the uploaded `schema.sql` file to ensure the LLM has perfect context of the tables, columns, and foreign keys.
   - `prompt_builder.py` wraps the schema and the user's question into strict instructions.
   - `sql_generator.py` queries Groq (Qwen 32B model).
   - `sql_validator.py` cleans up the LLM's response (stripping `<think>` blocks and markdown) and permanently blocks destructive commands like `DROP` or `UPDATE`.
   - `query_executor.py` executes the pure `SELECT` statement and returns both the SQL syntax and the raw table rows.
   - React beautifully renders the SQL code block and an HTML data table for the user.

---

## 💻 Local Development Setup

### 1. Requirements
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.
- [Node.js](https://nodejs.org/) installed.
- A free [Groq API Key](https://console.groq.com/keys).

### 2. Configure Environment
In the root directory, create a `.env` file:
```env
# Create .env and paste this exactly:
GROQ_API_KEY=gsk_your_key_here
DATABASE_URL=sqlite:///./test.db
```

### 3. Start the Backend
Open Terminal 1 in the project root:
```bash
uv pip install -e .
uv run uvicorn app.main:app --reload
```
*(Runs on http://localhost:8000)*

### 4. Start the Frontend
Open Terminal 2 in the `frontend/` folder:
```bash
cd frontend
npm install
npm run dev
```
*(Runs on http://localhost:5173)*

### 5. Start Chatting
Open your browser to `http://localhost:5173`. Drag and drop your `.csv` files and your `schema.sql` to instantly build the database and start talking to your data!

---

## ☁️ Production Deployment

This stack is designed to be hosted for **free** using Render and Vercel.

### Backend (Render.com)
1. Sign up for a free Web Service on Render.
2. Connect your GitHub repository.
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add `GROQ_API_KEY` to your Environment Variables.

### Frontend (Vercel.com)
1. Sign up for Vercel and import your GitHub repository.
2. Edit the "Root Directory" and select the `frontend/` folder.
3. Framework Preset: **Vite**.
4. Add Environment Variable:
   - Name: `VITE_API_URL`
   - Value: `https://your-render-url.onrender.com/api` *(Make sure to add /api)*
5. Deploy!
