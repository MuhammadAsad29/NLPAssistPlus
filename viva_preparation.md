# NLPAssist+ Viva Preparation Guide

This guide breaks down every component of the project to help you confidently answer questions during your viva.

## 1. High-Level Architecture
**"What did you build?"**
I built a **RAG (Retrieval-Augmented Generation) System**. This means the AI doesn't just guess answers; it "looks up" information in your specific documents before answering.

*   **Frontend**: React (User Interface for chatting).
*   **Backend**: Python FastAPI (Handles the logic).
*   **Brain**: Gemini API (`gemini-2.5-flash`) (The LLM that writes the answer).
*   **Memory**: FAISS + Sentence-Transformers (The systems that find relevant document chunks in our ~60+ Q/A dataset).

---

## 2. Core Concepts (The "Why" and "How")

### RAG (Retrieval-Augmented Generation)
*   **Concept**: Instead of asking ChatGPT directly, we first search our own data for relevant info, then paste that info into the prompt along with the user's question.
*   **Why use it?**: Standard LLMs (like GPT/Gemini) don't know about *your* specific university FAQs. RAG bridges that gap without needing expensive "fine-tuning."

### Embeddings (`all-MiniLM-L6-v2`)
*   **Concept**: Computers can't understand text like "fees." They only understand numbers. An "Embedding Model" turns text into a long list of numbers (a vector).
*   **Why this model?**: It's the industry standard for lightweight, local use. It's fast (CPU-friendly) and free.

### Vector Search (FAISS)
*   **Concept**: Once we have lists of numbers (vectors) for all our documents, we need to find which one is "closest" to the user's question vector.
*   **FAISS (Facebook AI Similarity Search)**: This is a library optimized to do that math incredibly fast.
*   **Why FAISS?**: It's faster than a simple Python loop and easier to set up than a full database for this project size.

---

## 3. Data Flow (Step-by-Step)

**Scenario: User asks "What is the policy?"**

1.  **Ingestion (Startup)**:
    *   `rag.py` reads `university_faq.txt`.
    *   It splits the text into chunks (paragraphs).
    *   It converts each chunk into a vector using `SentenceTransformer`.
    *   It stores these vectors in RAM using `FAISS`.

2.  **Retrieval**:
    *   User asks "What is the policy?" in frontend.
    *   Backend converts that question into a vector.
    *   FAISS finds the top 3 most similar chunk vectors from our stored list.

3.  **Generation**:
    *   We create a prompt: *"Universty Policy says X... User asked: What is the policy?"*
    *   We send this to **Gemini API**.
    *   Gemini generates the answer based *only* on the text we managed to find.
    *   **Generation Config**: We use `top_p=0.9` (diversity), `top_k=40` (focus), and `temperature=0.7` (creativity balance) to ensure natural yet accurate responses.

4.  **Response**:
    *   The answer is sent back to the React Frontend to display.

---

## 4. Code Structure Walkthrough

### `backend/main.py`
*   **Purpose**: The API Server. It accepts requests from the internet (Frontend).
*   **Key Part**: The `/ask` endpoint. This is the door where questions enter the system.

### `backend/rag.py`
*   **Purpose**: The Engine. It does all the heavy lifting.
*   **Key Functions**:
    *   `ingest_documents()`: The setup phase (reading files).
    *   `retrieve()`: The search phase (finding chunks).
    *   `generate_answer()`: The talking phase (calling Gemini).

### `frontend/`
*   **Purpose**: The Face. A simple chat interface.
*   **Key Tech**: React for building the UI, TailwindCSS for styling it nicely.

---

## 5. Potential tricky questions

**Q: Why isn't the data saved when I close the server?**
A: "For this prototype, I implemented an **in-memory vector store** to keep the architecture simple and lightweight. In a production environment, I would use a persistent database like ChromaDB or Pinecone."

**Q: Why didn't you use LangChain?**
A: "I wanted to demonstrate a deep understanding of the RAG pipeline by implementing the Retrieval and Generation logic manually using the underlying libraries (Sentence-Transformers and FAISS) rather than relying on a high-level abstraction."

**Q: How do you handle updated documents?**
A: "Currently, the system re-indexes on startup. A future improvement would be to implement an API endpoint that triggers re-indexing dynamically without restarting."
