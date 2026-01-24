import re
from data_store import get_alarm_by_code, search_alarm_by_description
from model import model, tokenizer

ALARM_REGEX = re.compile(r"\bAL[-\s]?\d+\b", re.IGNORECASE)

def detect_intent(question: str) -> str:
    q = question.lower()
    if any(x in q for x in ["how", "fix", "solution", "resolve"]):
        return "solution"
    if any(x in q for x in ["why", "reason", "cause"]):
        return "reason"
    if any(x in q for x in ["what", "explain", "meaning"]):
        return "explanation"
    return "general"

def ask_alarm_bot(question: str) -> str:
    question = question.strip()
    intent = detect_intent(question)

    alarm = None

    # Try alarm code
    match = ALARM_REGEX.search(question)
    if match:
        alarm_code = match.group().upper().replace("-", "").replace(" ", "")
        alarm = get_alarm_by_code(alarm_code)

    # Try description search
    if not alarm:
        alarm = search_alarm_by_description(question)

    # 🚨 IMPORTANT: Even if alarm not found, LLM will answer
    alarm_context = (
        f"Alarm Code: {alarm['Alarm Code']}\n"
        f"Description: {alarm['Description']}\n"
        f"Solution: {alarm['Solution']}"
        if alarm else
        "No exact alarm was found in the database."
    )

    # 🔥 CHATGPT-STYLE PROMPT (FORCES REASONING)
    prompt = f"""
    You are an industrial support engineer.

    Alarm information:
    Alarm Code: {alarm['Alarm Code']}
    Description: {alarm['Description']}
    Solution: {alarm['Solution']}

    User question:
    {question}

    Answer:
    """

    # 🔥 FORCE TinyLLaMA EXECUTION
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=180,
        temperature=0.7,
        do_sample=True,
        top_p=0.9
    )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if "Answer:" in decoded:
        decoded = decoded.split("Answer:")[-1].strip()

    return decoded

