import json 
from pathlib import Path 
with open("rawDocs/pytorch_docs.json","r",encoding="utf-8") as f : 
    docs = json.load(f)

OUTPUT_FILE = Path("rawDocs/chunks.json")

sections = []
current = None
for item in docs: 
    key = (item["title"],item["section"])
    
    if current is None or key != current["key"]:
        
        if current is not None:
            sections.append(current)
        
        current = {
            "key":key ,
            "title":item["title"],
            "section": item["section"],
            "url" : item["url"],
            "text": item["text"]
        }
    else:
        current["text"]+= "\n" + item["text"]
    
if current is not None:
    sections.append(current)    
    
print("Sections: ",len(sections))

chunks = []
MAX_WORDS = 400
OVERLAP = 50
for section in sections:
    words = section["text"].split()
    
    if len(words) <=400:
        chunks.append({
            "title": section["title"],
            "section": section["section"],
            "url": section["url"],
            "text": section["text"]
        })
        continue
    start = 0 
    
    while start<len(words):
        end = start + MAX_WORDS 
        chunk_words = words[start:end]
        chunks.append({
            "title": section["title"],
            "section": section["section"],
            "url": section["url"],
            "text": " ".join(chunk_words)
        })
        
        start += MAX_WORDS- OVERLAP
        
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)


print("Chunks:", len(chunks))
print(f"Saved to {OUTPUT_FILE}")