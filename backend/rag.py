import os
import glob
from typing import List, Dict, Tuple
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=API_KEY)

class RAGPipeline:
    def __init__(self, data_dir: str = "backend/data", embedding_model: str = "all-MiniLM-L6-v2"):
        self.data_dir = data_dir
        print(f"Loading embedding model: {embedding_model}...")
        self.embedder = SentenceTransformer(embedding_model)
        self.dimension = self.embedder.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(self.dimension)
        self.chunks: List[str] = []
        self.sources: List[str] = []
        self.is_indexed = False

    def ingest_documents(self):
        """Reads text files from data_dir, chunks them, and indexes embeddings."""
        print("Starting ingestion...")
        self.chunks = []
        self.sources = []

        files = glob.glob(os.path.join(self.data_dir, "*.txt"))
        if not files:
            print("No text files found in data directory.")
            return

        for file_path in files:
            file_name = os.path.basename(file_path)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            raw_chunks = text.split("\n\n")
            for chunk in raw_chunks:
                clean_chunk = chunk.strip()
                if len(clean_chunk) > 20:
                    self.chunks.append(clean_chunk)
                    self.sources.append(file_name)

        if not self.chunks:
            print("No valid chunks found.")
            return

        print(f"Encoding {len(self.chunks)} chunks...")
        embeddings = self.embedder.encode(self.chunks)

        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(np.array(embeddings).astype("float32"))

        self.is_indexed = True
        print(f"Ingestion complete. Indexed {len(self.chunks)} chunks.")

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        if not self.is_indexed:
            print("Index empty. Triggering ingestion.")
            self.ingest_documents()

        if not self.chunks:
            return []

        query_vector = self.embedder.encode([query])
        distances, indices = self.index.search(np.array(query_vector).astype("float32"), top_k)

        results = []
        for i, idx in enumerate(indices[0]):
            if 0 <= idx < len(self.chunks):
                results.append({
                    "text": self.chunks[idx],
                    "source": self.sources[idx],
                    "score": float(distances[0][i])
                })
        return results

    def generate_answer(self, query: str) -> Dict:
        retrieved_items = self.retrieve(query)

        if not retrieved_items:
            return {
                "answer": "I couldn't find any relevant information in my knowledge base to answer that.",
                "sources": []
            }

        context_str = "\n\n".join(
            [f"Source ({item['source']}):\n{item['text']}" for item in retrieved_items]
        )

        prompt = f"""You are NLPAssist+, a friendly university AI guide.

TASK:
Answer the user's question using the context below.

CRITICAL RULES:
1. NEVER copy the text exactly. You MUST rewrite it in your own words.
2. If the context is a Q&A pair like "Q: ... A: ...", convert it into a natural explanation.
3. Be helpful and polite.
4. If the context doesn't have the answer, say "I'm sorry, I don't see that in the university documents."

CONTEXT:
{context_str}

USER QUESTION: {query}
YOUR ANSWER:"""

        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    top_p=0.9,
                    top_k=20,
                    temperature=0.7
                )
            )
            answer_text = response.text
        except Exception as e:
            print(f"CRITICAL ERROR in generate_answer: {str(e)}")
            import traceback
            traceback.print_exc()
            answer_text = f"Error generating answer: {str(e)}"

        return {
            "answer": answer_text,
            "sources": [item['source'] for item in retrieved_items]
        }
