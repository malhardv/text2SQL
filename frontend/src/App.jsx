import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { UploadCloud, MessageSquare, Database, CheckCircle2, Loader2, Send, FileCode2, Table } from 'lucide-react';
import './index.css';

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

function App() {
  const [isSetupComplete, setIsSetupComplete] = useState(false);
  const [schemaFile, setSchemaFile] = useState(null);
  const [csvFiles, setCsvFiles] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState("");

  const [messages, setMessages] = useState([]);
  const [inputVal, setInputVal] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSchemaDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer ? e.dataTransfer.files[0] : e.target.files[0];
    if (file && file.name.endsWith('.sql')) {
      setSchemaFile(file);
    } else {
      setUploadError("Please upload a .sql schema file.");
    }
  };

  const handleCsvDrop = (e) => {
    e.preventDefault();
    const files = e.dataTransfer ? Array.from(e.dataTransfer.files) : Array.from(e.target.files);
    const validCsvs = files.filter(f => f.name.endsWith('.csv'));
    if (validCsvs.length > 0) {
      setCsvFiles(prev => [...prev, ...validCsvs]);
      setUploadError("");
    } else {
      setUploadError("Please upload .csv files only.");
    }
  };

  const handleSetupSubmit = async () => {
    if (!schemaFile) {
      setUploadError("Schema (.sql) file is missing.");
      return;
    }
    if (csvFiles.length === 0) {
      setUploadError("At least one CSV file is required.");
      return;
    }

    setIsUploading(true);
    setUploadError("");

    const formData = new FormData();
    formData.append("schema_file", schemaFile);
    csvFiles.forEach(file => {
      formData.append("csv_files", file);
    });

    try {
      const resp = await axios.post(`${API_BASE}/setup`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      console.log(resp.data);
      setIsSetupComplete(true);
      setMessages([{
        role: "assistant",
        content: `Database successfully loaded! ${resp.data.tables_imported} tables created. How can I help you query your data today?`
      }]);
    } catch (err) {
      console.error(err);
      setUploadError(err.response?.data?.detail || "An error occurred during upload.");
    } finally {
      setIsUploading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputVal.trim() || isTyping) return;

    const userMsg = inputVal.trim();
    setMessages(prev => [...prev, { role: "user", content: userMsg }]);
    setInputVal("");
    setIsTyping(true);

    try {
      const resp = await axios.post(`${API_BASE}/query`, { question: userMsg });
      const data = resp.data;

      setMessages(prev => [...prev, {
        role: "assistant",
        content: "Here are the results:",
        sql: data.generated_sql,
        columns: data.columns,
        rows: data.rows
      }]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, {
        role: "assistant",
        error: true,
        content: err.response?.data?.detail || "Sorry, I encountered an error generating the SQL query."
      }]);
    } finally {
      setIsTyping(false);
    }
  };

  // --- RENDERING VIEWS ---

  if (!isSetupComplete) {
    return (
      <div className="app-container setup-view">
        <div className="glass-panel setup-panel">
          <div className="setup-header">
            <Database className="icon-large pulse" />
            <h1>Initialize Database</h1>
            <p>Upload your data to start generating SQL from natural language.</p>
          </div>

          <div className="upload-zones">
            {/* Schema Upload */}
            <div
              className={`upload-zone ${schemaFile ? 'success' : ''}`}
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleSchemaDrop}
            >
              <input type="file" accept=".sql" id="schema-upload" hidden onChange={handleSchemaDrop} />
              <label htmlFor="schema-upload" className="upload-label">
                {schemaFile ? <CheckCircle2 className="icon-success" /> : <FileCode2 className="icon-base" />}
                <div className="upload-text">
                  <h3>{schemaFile ? "Schema Ready" : "Upload Schema (.sql)"}</h3>
                  <p>{schemaFile ? schemaFile.name : "Drag & drop or click to browse"}</p>
                </div>
              </label>
            </div>

            {/* CSV Data Upload */}
            <div
              className={`upload-zone ${csvFiles.length > 0 ? 'success' : ''}`}
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleCsvDrop}
            >
              <input type="file" accept=".csv" multiple id="csv-upload" hidden onChange={handleCsvDrop} />
              <label htmlFor="csv-upload" className="upload-label">
                {csvFiles.length > 0 ? <CheckCircle2 className="icon-success" /> : <Table className="icon-base" />}
                <div className="upload-text">
                  <h3>{csvFiles.length > 0 ? `${csvFiles.length} CSVs Ready` : "Upload Data (.csv)"}</h3>
                  <p>{csvFiles.length > 0 ? csvFiles.map(f => f.name).join(', ') : "Drag & drop multiple files or click to browse"}</p>
                </div>
              </label>
            </div>
          </div>

          {uploadError && <div className="error-message">{uploadError}</div>}

          <button
            className="btn-primary start-btn"
            onClick={handleSetupSubmit}
            disabled={isUploading || !schemaFile || csvFiles.length === 0}
          >
            {isUploading ? <><Loader2 className="spin" /> Building Database...</> : "Start Chatting"}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container chat-view">
      <div className="chat-header">
        <Database className="icon-sm" />
        <h2>Database Chat Assistant</h2>
      </div>

      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message-wrapper ${msg.role}`}>
            <div className="message-avatar">
              {msg.role === 'user' ? "U" : <MessageSquare className="icon-xs" />}
            </div>
            <div className={`message-bubble ${msg.error ? 'error' : ''}`}>
              <p>{msg.content}</p>

              {msg.sql && (
                <div className="sql-block">
                  <div className="sql-header">Generated SQL</div>
                  <code>{msg.sql}</code>
                </div>
              )}

              {msg.columns && msg.rows && msg.rows.length > 0 && (
                <div className="table-responsive">
                  <table className="data-table">
                    <thead>
                      <tr>
                        {msg.columns.map((col, i) => <th key={i}>{col}</th>)}
                      </tr>
                    </thead>
                    <tbody>
                      {msg.rows.map((row, rowIdx) => (
                        <tr key={rowIdx}>
                          {msg.columns.map((col, colIdx) => (
                            <td key={colIdx}>{row[col]}</td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              {msg.columns && msg.rows && msg.rows.length === 0 && (
                <div className="no-data">No rows returned.</div>
              )}
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="message-wrapper assistant typing">
            <div className="message-avatar"><Loader2 className="icon-xs spin" /></div>
            <div className="typing-indicator">Querying database...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <form onSubmit={handleSendMessage} className="input-form glass-panel">
          <input
            type="text"
            placeholder="Ask a question about your database..."
            value={inputVal}
            onChange={(e) => setInputVal(e.target.value)}
            disabled={isTyping}
          />
          <button type="submit" disabled={!inputVal.trim() || isTyping} className="send-btn">
            <Send className="icon-sm" />
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
