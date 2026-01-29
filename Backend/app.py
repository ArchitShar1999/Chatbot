from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from io import BytesIO

from rag import ask_alarm_bot
from vectorstore import ingest_excel

app = FastAPI(title="Alarm Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# MODELS
# -----------------------
class Query(BaseModel):
    question: str

# -----------------------
# HEALTH CHECK
# -----------------------
@app.get("/")
def root():
    return {"status": "running"}

# -----------------------
# UPLOAD EXCEL (TRAIN / INGEST)
# -----------------------
@app.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(400, "Only .xlsx files allowed")

    raw = await file.read()
    df = pd.read_excel(BytesIO(raw))

    ingest_excel(df)

    return {
        "status": "success",
        "rows_indexed": len(df),
        "message": "Excel uploaded. You can now ask questions."
    }

# -----------------------
# ASK QUESTIONS
# -----------------------
@app.post("/ask")
def ask(query: Query):
    answer = ask_alarm_bot(query.question)

    return {
        "question": query.question,
        "answer": answer
    }
