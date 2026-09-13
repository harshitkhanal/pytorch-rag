from fastapi import FastAPI 
from pydantic import BaseModel 
from generation import generate_answer
from fastapi.middleware.cors import CORSMiddleware
app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List specific domains for production (e.g., ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)
class Query(BaseModel):
    query:str 

@app.post("/ask")
def ask_question(data:Query):
    answer = generate_answer(data.query)
    return {
        "answer":answer
    }