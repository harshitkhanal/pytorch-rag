# PyTorch RAG 

A Retrieval-Augmented Generation (RAG) chat app that answers questions about PyTorch using content scraped from PyTorch documentation sources, rather than relying on the LLM's raw knowledge alone.

Ask a question → relevant doc chunks are retrieved via semantic search → an LLM generates an answer grounded in those chunks, with sources cited.

## How it works

1. **Scrape** — `scrape.py` and `scrape1.py` each pull content from a PyTorch documentation source (including [learnpytorch.io](https://www.learnpytorch.io/)), saving raw pages and chunked JSON into `raw_docs/` and `rawDocs/` respectively.
2. **Combine** — `combine_chunks.py` merges both sources' chunks into a single `docs/chunks.json`.
3. **Embed** — `embed.py` generates sentence embeddings for every chunk using `sentence-transformers/all-MiniLM-L6-v2`, saved as `docs/embeddings.npy`.
4. **Index** — `build_index.py` builds a FAISS index from those embeddings, saved as `docs/pytorch.index`.
5. **Retrieve** — at query time, `retreiver.py` embeds the user's question and searches the FAISS index for the top-3 most relevant chunks.
6. **Generate** — `generation.py` builds a prompt from the retrieved chunks and calls the Gemini API to produce a grounded answer, with source links appended. To stretch free-tier daily quotas, it randomly tries across three Gemini models (`gemini-3.5-flash`, `gemini-3.5-flash-lite`, `gemini-2.5-flash`) with fallback if one is rate-limited.
7. **Serve** — `api/api.py` is a FastAPI backend exposing a single `POST /ask` endpoint.
8. **Chat UI** — `frontend/` is a React + Vite app with a ChatGPT-style interface: multiple chat threads (persisted in localStorage), markdown-rendered answers, and source citations.

## Tech stack

**Frontend:** React, Vite, Tailwind CSS, axios, react-markdown, lucide-react
**Backend:** FastAPI (Python)
**Retrieval:** sentence-transformers, FAISS
**Generation:** Google Gemini API (`google-genai`)

## Project structure

```
pytorch-rag/
├── api/
│   ├── api.py           # FastAPI app (POST /ask)
│   └── requirements.txt
├── docs/                 # combined, embedded, and indexed doc chunks
├── frontend/              # React + Vite chat UI
├── raw_docs/              # scraped output from scrape.py
├── rawDocs/                # scraped output from scrape1.py
├── scrape.py
├── scrape1.py
├── combine_chunks.py
├── chunker.py
├── embed.py
├── build_index.py
├── generation.py
├── retreiver.py
└── .gitignore
```

## Setup

### Backend

```bash
git clone https://github.com/harshitkhanal/pytorch-rag.git
cd pytorch-rag

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r api/requirements.txt
```

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

The repo already includes a pre-built `docs/chunks.json`, `docs/embeddings.npy`, and `docs/pytorch.index`, so you can run the app immediately without re-scraping. If you want to rebuild the index from scratch (e.g. after adding new sources), run:

```bash
python scrape.py
python scrape1.py
python combine_chunks.py
python embed.py
python build_index.py
```

Start the backend:
```bash
uvicorn api.api:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
```

Create a `.env` file in `frontend/`:
```
VITE_API_URL=http://127.0.0.1:8000
```

Start the dev server:
```bash
npm run dev
```

## Notes

- This project uses Gemini's free tier, which has a low daily request cap per model. The model-fallback logic in `generation.py` helps stretch that limit, but heavy use may still hit rate limits.
- Not currently deployed live — run locally following the steps above.

## Sources

Doc content is sourced from PyTorch-related documentation sites, chunked by section, with each answer citing the specific section and URL it drew from.