import json 
import numpy as np 
import faiss 


with open("docs/chunks.json","r",encoding="utf-8") as f : 
    chunks = json.load(f)
    
embeddings = np.load("docs/embeddings.npy")

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)
index.add(embeddings)


faiss.write_index(index,"docs/pytorch.index")
    