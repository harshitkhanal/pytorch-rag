import requests 
from bs4 import BeautifulSoup 
import json 

DOCS = {
    "Pytorch_Fundamentals":"https://www.learnpytorch.io/00_pytorch_fundamentals/",
    "PytorchWorkflow":"https://www.learnpytorch.io/01_pytorch_workflow/",
    "NeuralNetworkClassification":"https://www.learnpytorch.io/02_pytorch_classification/",
    "PytorchVision":"https://www.learnpytorch.io/03_pytorch_computer_vision/",
    "CustomDatasets":"https://www.learnpytorch.io/04_pytorch_custom_datasets/",
    "TransferLearning":"https://www.learnpytorch.io/06_pytorch_transfer_learning/"
}


def scrape_data(title,url):
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text,"html.parser")
    main = soup.find("main")
    if main is None:
        raise Exception(f"Couldnt find content in {url}")
    
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
                    "section":curr_section.replace(" ¶", ""),
                    "url":url , 
                    "text":text
                })
    return sections

all_docs = []

for title,url in DOCS.items():
    print(f"Scraping {title}")
    try:
      sections = scrape_data(title,url)
      all_docs.extend(sections) 
      print(f"-> {len(sections)} pieces")
      
    except:
      print('An exception occurred')
    

with open("rawDocs/pytorch_docs.json","w",encoding="utf-8") as f : 
    json.dump(all_docs,f,indent=2,ensure_ascii=False)

print(f"\nTotal pieces: {len(all_docs)}")
print("Saved to rawDocs/pytorch_docs.json")