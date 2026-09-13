from google import genai
from dotenv import load_dotenv
import os
import random
import re
from retreiver import retrieve_info

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
models = ["gemini-3.5-flash","gemini-3.5-flash-lite","gemini-2.5-flash","gemini-3-flash","gemini-3.7-flash"]
def generate_answer(query):
    retrived_chunks = retrieve_info(query) 
    context = ""
    for i,chunk in enumerate(retrived_chunks,1):
        context +=f"""
        ---Context{i}---
        section:{chunk["section"]}
        Source:{chunk["url"]}
        {chunk["text"]}        
        """
        
    prompt = f"""
          You are answering a technical question about PyTorch using ONLY the context passages below.

Rules:
- Answer using information from the context only. If the context doesn't contain the answer, say so — don't guess.
- Write the answer in your own words. Do not copy phrasing directly from the context, and if multiple passages restate the same idea, mention it once — don't stitch their wordings together.
- Keep it concise: a short explanation, plus a code snippet if the context includes relevant code.
            Context:
            {context}

            User question:
            {query}
            """
    models_shuffled = random.sample(models,len(models))
    interaction = None
    for model in models_shuffled:
        try:
           interaction = client.interactions.create(
            model=random.choice(models),
            input=prompt
        )
           break
        except Exception as e :
            print(f"{model} failed : {e}")   
            continue     
    if interaction is None:
        return "All models are currently rate-limited. Try again later."
    
   
    sources = "\n\nSources:\n"

    for i, chunk in enumerate(retrived_chunks, 1):
        sources += f"[{i}] {chunk['section']}\n{chunk['url']}\n"
    return interaction.output_text + sources

