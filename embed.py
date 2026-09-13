import json 
from sentence_transformers import SentenceTransformer
import numpy as np
with open("docs/chunks.json","r",encoding="utf-8") as f : 
    chunks = json.load(f)

print("Chunks: ",len(chunks))

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2") 

texts = [chunk["text"] for chunk in chunks]


embeddings = model.encode(
    texts,
    normalize_embeddings = True,
    show_progress_bar=True 
)

np.save("docs/embeddings.npy",embeddings)
print("Saved")
