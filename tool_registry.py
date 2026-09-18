from dataclasses import dataclass
from typing import Callable, Any
import re

@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    category: str
    required: tuple[str, ...]
    handler: Callable[[dict[str, Any]], str]
    side_effecting: bool = False

class ToolRegistry:
    """Metadata-first registry. Prototype retrieval is lexical; production should use hybrid search."""
    def __init__(self):
        self.tools: dict[str, Tool] = {}
        self.register_defaults()

    def register(self, tool: Tool):
        if tool.name in self.tools:
            raise ValueError(f"Duplicate tool name: {tool.name}")
        self.tools[tool.name] = tool

    def get(self, name: str):
        return self.tools.get(name)

    def discover(self, query: str, limit: int = 5) -> list[Tool]:
        tokens = {t for t in re.findall(r"[a-zA-Z0-9_]+", query.lower()) if len(t) > 2}
        scored = []
        for tool in self.tools.values():
            searchable = set(re.findall(
                r"[a-zA-Z0-9_]+",
                f"{tool.name} {tool.description} {tool.category}".lower()
            ))
            score = len(tokens & searchable)
            if score:
                scored.append((score, tool.name, tool))
        scored.sort(key=lambda row: (-row[0], row[1]))
        return [row[2] for row in scored[:limit]]

    def execute(self, name: str, args: dict[str, Any]) -> str:
        tool = self.get(name)
        if tool is None:
            return f"Error: unknown tool '{name}'."
        missing = [key for key in tool.required if args.get(key) in (None, "")]
        if missing:
            return "Please provide: " + ", ".join(missing) + "."
        if "amount" in args:
            try:
                amount = float(args["amount"])
                if amount <= 0:
                    return "Validation error: amount must be greater than zero."
                args["amount"] = amount
            except (TypeError, ValueError):
                return "Validation error: amount must be numeric."
        return tool.handler(args)

    def catalog_text(self):
        return "\n".join(
            f"{t.name} [{t.category}] — {t.description}" for t in self.tools.values()
        )

    def register_defaults(self):
        self.register(Tool(
            "paypal_create_invoice",
            "Create a draft invoice for a recipient and amount.",
            "invoice billing",
            ("recipient", "amount"),
            lambda a: f"MOCK ONLY: draft invoice prepared for {a['recipient']} for ${a['amount']:.2f}; no real invoice sent."
        ))
        self.register(Tool(
            "paypal_sales_report",
            "Retrieve sales volume report for a requested period.",
            "reports analytics sales",
            ("period",),
            lambda a: f"MOCK ONLY: no live sales data available for {a['period']}."
        ))
        self.register(Tool(
            "paypal_find_dispute",
            "Check dispute status for a user or customer identifier.",
            "disputes customer",
            ("user_id",),
            lambda a: f"MOCK ONLY: no live dispute lookup performed for {a['user_id']}."
        ))
        self.register(Tool(
            "paypal_send_payment",
            "Send money to a recipient; requires authorization and explicit confirmation.",
            "payments transfer",
            ("recipient", "amount"),
            lambda a: "Blocked in prototype: real payment execution is disabled.",
            side_effecting=True
        ))
