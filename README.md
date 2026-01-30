# Alarm Chatbot (FastAPI + RAG + LLM)

A **Retrieval‑Augmented Generation (RAG) based Alarm Chatbot** built with **FastAPI**, **ChromaDB**, and a **local LLM (llama.cpp)**.
The system allows users to upload alarm data via Excel files and ask questions to get **fast, reliable, and domain‑specific answers**.

This project is structured into a **Backend (API + RAG logic)** and a **Frontend (Web UI)**.

---

## 📁 Project Structure

```
Chatbot/
├── Backend/
│   ├── Model/
│   ├── app.py              # FastAPI entry point
│   ├── ingest.py           # Excel ingestion script
│   ├── model.py            # LLM loading (llama.cpp)
│   ├── rag.py              # RAG logic (prompt + LLM call)
│   └── vectorstore.py      # ChromaDB & embedding logic
│
├── Frontend/
│   ├── icons/              # UI icons
│   ├── Beumer_logo_W.png
│   ├── Logo-BEUMER-Group.webp
│   ├── app.js              # Frontend logic
│   ├── index.html          # Main UI
│   └── style.css           # Styling
│
└── README.md
```

---

## 🚀 Features

* Upload alarm data using Excel (`.xlsx`)
* Strict alarm code validation (no guessing)
* Vector‑based semantic search (ChromaDB)
* Exact alarm code matching for ultra‑fast lookup
* Local LLM inference (CPU‑only, fast & secure)
* Clean web‑based frontend UI

---

## ⚙️ Backend Overview

### `app.py`

* FastAPI application entry point
* Exposes APIs:

  * `/upload-excel` → Upload & ingest Excel
  * `/ask` → Ask alarm‑related questions

---

### `ingest.py`

* Command‑line Excel ingestion utility
* Validates:

  * File existence
  * `.xlsx` format
  * Required columns (`alarm no`, `alarm description`)
* Loads data into the vector database

---

### `vectorstore.py`

* Handles:

  * Alarm code cleaning & validation
  * Embedding generation
  * ChromaDB storage & retrieval
* Supports:

  * Exact alarm code search (metadata filter)
  * Semantic search (description‑based)

---

### `model.py`

* Loads the local LLM using **llama.cpp**
* Optimized for speed:

  * Small context window
  * CPU‑only execution
  * Low memory usage

---

### `rag.py`

* Core RAG logic
* Builds a strict system prompt
* Sends retrieved alarm context to the LLM
* Ensures:

  * No hallucinations
  * Short, practical answers
  * Engineer‑style responses

---

## 🌐 Frontend Overview

The frontend is a lightweight web UI built with **HTML, CSS, and JavaScript**.

### Key Files

* `index.html` → Page structure
* `style.css` → Styling & layout
* `app.js` → API calls & chat logic
* `icons/` → UI icons
* Logos included for branding

The frontend communicates with the FastAPI backend using HTTP requests.

---

## 🧠 How the System Works

### 1️⃣ Excel Upload Flow

1. User uploads `.xlsx` file
2. Backend validates file & columns
3. Alarm rows converted into documents
4. Embeddings generated
5. Stored in ChromaDB

### 2️⃣ Question Answer Flow

1. User asks a question
2. Alarm code detected (if present)
3. Exact match or semantic search
4. Context retrieved from vector DB
5. LLM generates grounded answer
6. Answer returned to UI

---

## 🧪 Example API Usage

### Upload Excel

```
POST /upload-excel
```

### Ask Question

```json
{
  "question": "What is AL4024?"
}
```

---

## 🛠️ Setup Instructions

### 0️⃣ Model Requirement

This project uses a **local LLM model**:

```
mistral-7b-instruct-v0.1.Q4_K_M.gguf
```

**Steps:

### 0️⃣ Model Requirement

This project uses a **local LLM model**:

```
mistral-7b-instruct-v0.1.Q4_K_M.gguf
```

**Steps:**

1. Create a folder named `models` inside `Backend`
2. Download the model file
3. Place it here:

```
Backend/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf
```

> ⚠️ The application will not start if the model f

### 1. Clone Repository

```bash
git clone https://github.com/ArchitShar1999/Chatbot.git
cd Chatbot
```

### 2. Backend Setup

#### Step 1: Create Virtual Environment

```bash
cd Backend
python -m venv .venv
```

#### Step 2: Activate Virtual Environment

```bash
.\\.venv\\Sc

---

## ⚡ Performance Highlights

- Exact alarm lookup before semantic search
- Small LLM context (fast inference)
- Low temperature (reliable answers)
- No internet dependency
- Optimized for real‑time operations

---

## 📄 License

MIT License

---

## 👤 Author

**Archit Sharma**  
MCA | System & Automation Enthusiast  

---

## 🔚 One‑Line Summary

**Excel → Validate → Embed → ChromaDB → Retrieve → LLM → Answer**

```
