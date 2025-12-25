# NLPAssist+

NLPAssist+ is a Retrieval-Augmented Generation (RAG) powered Question Answering system.

## Prerequisites
- Python 3.8+
- [Node.js & npm](https://nodejs.org/) (Required for Frontend)
- [Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist) (Required for PyTorch/Backend)

## Setup

### Backend
1. Navigate to `backend/`:
   ```sh
   cd backend
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the server:
   ```sh
   uvicorn main:app --reload
   ```
   Server will start at `http://localhost:8000`.

### Frontend
1. Navigate to `frontend/`:
   ```sh
   cd frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Run the development server:
   ```sh
   npm run dev
   ```
   Open the link shown (usually `http://localhost:5173`).

## Usage
- The system pre-loads `backend/data/university_faq.txt` into the vector store on startup.
- You can add more `.txt` files to `backend/data/` and restart the server (or call `POST /ingest`).
- Use the Chat UI to ask questions.

## Architecture
- **Backend**: FastAPI, SentenceTransformers, FAISS, Google Gemini API.
- **Frontend**: React, Vite, TailwindCSS.
