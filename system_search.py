def system_search(query: str, registry, history: list[dict]) -> str:
    q = query.lower()
    if any(term in q for term in ("status", "last request", "history", "recent")):
        if not history:
            return "No requests recorded in this session yet."
        return "Recent session requests:\n" + "\n".join(
            f"- {item['request']} → {item['result']}" for item in history[-5:]
        )
    matches = registry.discover(query, limit=10)
    if not matches:
        return "No matching tools found in this demo catalog."
    return "Matching tools:\n" + "\n".join(
        f"- {tool.name}: {tool.description}" for tool in matches
    )
