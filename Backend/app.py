from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag import ask_alarm_bot

# ✅ CREATE FastAPI app (THIS WAS MISSING / WRONG)
app = FastAPI(
    title="Alarm Detection API",
    version="1.0"
)

# ✅ ADD CORS AFTER app IS CREATED
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "Backend is running"}

@app.post("/ask")
def ask(query: Query):
    return {
        "question": query.question,
        "answer": ask_alarm_bot(query.question)
    }
