from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
import re
import pandas as pd

PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "alarm_knowledge"

embeddings = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# -------------------------
# Helpers
# -------------------------
def _clean_alarm_code(value) -> str | None:
    if pd.isna(value):
        return None
    text = str(value).strip().upper()
    # remove .0 from Excel numeric cells
    text = re.sub(r"\.0$", "", text)
    # must contain at least one letter + digits
    if not re.match(r"^[A-Z]{1,3}\d{3,6}$", text):
        return None
    return text


# -------------------------
# INGEST EXCEL
# -------------------------
def ingest_excel(df: pd.DataFrame):
    # Normalize column names ONLY
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(".", "", regex=False)
    )

    required = {"alarm no", "alarm description"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )

    # 🔥 HARD RESET
    try:
        vectorstore._collection.delete(where={})
    except Exception:
        pass

    docs = []

    for _, row in df.iterrows():
        alarm_code = _clean_alarm_code(row["alarm no"])
        if not alarm_code:
            continue  # skip invalid rows

        description = str(row["alarm description"]).strip()

        solution = ""
        if "solution" in df.columns and pd.notna(row.get("solution")):
            solution = str(row["solution"]).strip()

        if not solution:
            solution = "No solution provided."

        docs.append(
            Document(
                page_content=(
                    f"Alarm Code: {alarm_code}\n"
                    f"Description: {description}\n"
                    f"Solution: {solution}"
                ),
                metadata={
                    "alarm_code": alarm_code
                }
            )
        )

    if not docs:
        raise ValueError("No valid alarm codes found in Excel")

    vectorstore.add_documents(docs)
    vectorstore.persist()


# -------------------------
# SEARCH CONTEXT
# -------------------------
def _extract_alarm_code(text: str) -> str | None:
    m = re.search(r"\b[A-Z]{1,3}\d{3,6}\b", text.upper())
    return m.group() if m else None


def search_context(query: str) -> str:
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )

    alarm_code = _extract_alarm_code(query)

    # 🔒 EXACT MATCH BY METADATA (CORRECT WAY)
    if alarm_code:
        results = vectorstore.similarity_search(
            query="dummy",  # ignored
            k=1,
            filter={"alarm_code": alarm_code}
        )
        return results[0].page_content if results else ""

    # 🔵 Semantic search for description queries
    results = vectorstore.similarity_search(query, k=1)
    return results[0].page_content if results else ""
