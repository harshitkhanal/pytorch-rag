from sentence_transformers import SentenceTransformer 
import json
import faiss
import re
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2") 

query = "Why do I need to call optimizer.zero_grad()?"

def get_embed(query):
    query_embed = model.encode(
        [query],
        show_progress_bar=True
    )
    return query_embed

def get_chunks():
    with open("docs/chunks.json","r",encoding="utf-8") as f :
        chunks = json.load(f) 
    return chunks
def retrieve_info(query):
    query = re.sub(r"\bin\s+PyTorch\b", "", query, flags=re.IGNORECASE)
    query = " ".join(query.split()) 
    query_embed = get_embed(query)
    index = faiss.read_index("docs/pytorch.index")
    scores,indices= index.search(query_embed,3)
    chunks= get_chunks()
    return [
    {
        "text": chunks[idx]["text"],
        "section": chunks[idx]["section"],
        "url": chunks[idx]["url"],
        "score": float(score)
    }
    for idx, score in zip(indices[0], scores[0])
]
    
