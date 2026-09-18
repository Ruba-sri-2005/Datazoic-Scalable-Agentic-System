import re
from tool_registry import ToolRegistry
from knowledge import rag_search
from system_search import system_search

class Agent:
    def __init__(self):
        self.registry = ToolRegistry()
        self.history: list[dict] = []
        self.state = {"turn_count": 0, "pending_action": None}

    def handle(self, message: str) -> str:
        self.state["turn_count"] += 1
        text = message.strip()
        low = text.lower()
        if not text:
            return "Please enter a request."

        if any(p in low for p in ("what tools", "available tools", "tool for", "last request", "request history", "status of my")):
            result = system_search(text, self.registry, self.history)
        elif any(p in low for p in ("how do i", "documentation", "guide", "explain", "what is", "how to")):
            result = "RAG result:\n" + rag_search(text)
        else:
            result = self._route_action(text, low)

        self.history.append({"request": text, "result": result})
        return result

    def _route_action(self, text: str, low: str) -> str:
        if "invoice" in low:
            amount_match = re.search(r"\$\s*(\d+(?:\.\d{1,2})?)", text)
            recipient_match = re.search(r"\bto\s+([\w.@+-]+)", text, re.I)
            args = {}
            if amount_match:
                args["amount"] = amount_match.group(1)
            if recipient_match:
                args["recipient"] = recipient_match.group(1).rstrip(".,")
            self.state["pending_action"] = "paypal_create_invoice"
            return self.registry.execute("paypal_create_invoice", args)

        if "dispute" in low:
            match = re.search(r"user_[A-Za-z0-9_-]+", text)
            args = {"user_id": match.group(0)} if match else {}
            return self.registry.execute("paypal_find_dispute", args)

        if "sales" in low or "sales volume" in low:
            period = "last month" if "last month" in low else "unspecified period"
            return self.registry.execute("paypal_sales_report", {"period": period})

        if "payment" in low or "send money" in low:
            return "Payment tool identified, but execution is disabled. A production system must authenticate, preview details, obtain explicit confirmation, and verify the provider response."

        candidates = self.registry.discover(text)
        if candidates:
            return "Potentially relevant tools: " + ", ".join(t.name for t in candidates) + ". Please clarify the exact action."
        return "I could not confidently identify a tool. Please clarify your request."

