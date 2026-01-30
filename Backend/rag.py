from vectorstore import search_context
from model import llm

SYSTEM_PROMPT = (
    "You are an airport baggage handling system engineer.\n"
    "Rules:\n"
    "- Use only the given alarm description.\n"
    "- Never say you are unaware or that data is missing.\n"
    "- Give a short, practical airport baggage handling solution.\n"
    "- Do not invent alarm codes or systems.\n"
)

def ask_alarm_bot(question: str) -> str:
    context = search_context(question)

    if not context:
        return "Alarm code not found in the uploaded Excel."

    prompt = f"""[INST]
{SYSTEM_PROMPT}

Alarm details:
{context}

Question:
{question}
[/INST]
"""

    response = llm(
        prompt,
        max_tokens=120,       # 🔥 FAST
        temperature=0.1,     # 🔒 reliable
        top_p=0.9,
        stop=["</s>"]
    )

    answer = response["choices"][0]["text"].strip()

    return answer
