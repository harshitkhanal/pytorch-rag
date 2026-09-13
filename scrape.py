from bs4 import BeautifulSoup 
import requests
import sys
from pathlib import Path
import json
sys.stdout.reconfigure(encoding='utf-8')   


BASE_URL = "https://docs.pytorch.org/docs/2.14/"


DOCS = {
    "tensors": "torch.Tensor",
    "autograd": "Autograd",
    "nn": "torch.nn",
    "loss": "Loss Functions",
    "optim": "Optimizers",
    "data": "Datasets & DataLoaders",
    "notes/serialization": "Saving & Loading Models",
}


def scrape(path,title):
    
    url = BASE_URL + path + ".html"
    
    response = requests.get(url) 
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text,"html.parser") 
    
    main = soup.find("main")
    if main is None:
        raise Exception(f"Could not find main content in {url}")

    for tag in main.find_all(["script","style","nav"]):
        tag.decompose()
    
    sections = []
    curr_section = title 
    
    for element in main.find_all(["h1","h2","h3","h4","p","li","pre"]):
        if element.name in ["h1","h2","h3","h4"]:
            curr_section = element.get_text(" ",strip =True)
        else:
            text = element.get_text(" ",strip = True)
            
            if text: 
                sections.append({
                    "title":title,
                    "section":curr_section,
                    "url":url , 
                    "text":text
                })
    return sections

Path("raw_docs").mkdir(exist_ok=True) 

all_docs = []

for path,title in DOCS.items():
    print(f"Scraping {title}")
    try:
      sections = scrape(path,title)
      all_docs.extend(sections) 
      print(f"-> {len(sections)} pieces")
      
    except:
      print('An exception occurred')

with open("raw_docs/pytorch_docs.json","w",encoding="utf-8") as f : 
    json.dump(all_docs,f,indent=2,ensure_ascii=False)
    
print(f"\nTotal pieces: {len(all_docs)}")
print("Saved to raw_docs/pytorch_docs.json")