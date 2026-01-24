import pandas as pd
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

EXCEL_PATH = "alarm_database.xlsx"

# Load Excel
df = pd.read_excel(EXCEL_PATH)

documents = []

for _, row in df.iterrows():
    text = f"""
Alarm Code: {row['Alarm No.']}
Description: {row['Alarm Description']}
Solution: {row['Solution']}
"""
    documents.append(text)

# Embeddings
embeddings = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# Store in Chroma
db = Chroma.from_texts(
    texts=documents,
    embedding=embeddings,
    persist_directory="alarm_db"
)

db.persist()
print("✅ Excel ingested into ChromaDB")
