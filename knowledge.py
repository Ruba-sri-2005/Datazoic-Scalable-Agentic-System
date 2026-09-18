# Small illustrative knowledge base; production should index approved documentation.
DOCUMENTS = [
    {"topic":"invoice", "text":"To create an invoice, collect recipient and amount, validate them, and preview the action before calling a provider API."},
    {"topic":"payments", "text":"Payments are side-effecting. Production systems should authenticate and authorize the user, show recipient and amount, require explicit confirmation, and use an idempotency key."},
    {"topic":"disputes", "text":"Dispute lookup should use a supported dispute or customer reference and only return records the authenticated user may access."},
    {"topic":"scaling", "text":"For large tool catalogs, retrieve relevant tool metadata and pass only a small top-k candidate set to the model rather than exposing every tool definition."},
]

def rag_search(question: str) -> str:
    words = {w.lower() for w in question.replace("?", "").split() if len(w) > 3}
    ranked = []
    for doc in DOCUMENTS:
        haystack = (doc["topic"] + " " + doc["text"]).lower()
        score = sum(1 for word in words if word in haystack)
        if score:
            ranked.append((score, doc))
    ranked.sort(key=lambda x: x[0], reverse=True)
    if not ranked:
        return "No matching passage found in the demo knowledge base."
    return "\n".join(f"[{d['topic']}] {d['text']}" for _, d in ranked[:3])
