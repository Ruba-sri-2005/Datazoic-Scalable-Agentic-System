import unittest
from agent import Agent
from tool_registry import Tool, ToolRegistry

class AgentTests(unittest.TestCase):
    def setUp(self):
        self.agent = Agent()

    def test_invoice_missing_fields(self):
        result = self.agent.handle("Create an invoice")
        self.assertIn("recipient", result)
        self.assertIn("amount", result)

    def test_mock_invoice(self):
        result = self.agent.handle("Create an invoice for $50 to alex@example.com")
        self.assertIn("MOCK ONLY", result)
        self.assertIn("alex@example.com", result)

    def test_nonpositive_amount_rejected(self):
        result = self.agent.handle("Create an invoice for $0 to alex@example.com")
        self.assertIn("greater than zero", result)

    def test_rag_route(self):
        self.assertIn("RAG result", self.agent.handle("How do I create an invoice?"))

    def test_system_search(self):
        self.assertIn("paypal_create_invoice", self.agent.handle("What tools are available for invoices?"))

    def test_unknown_request(self):
        self.assertIn("clarify", self.agent.handle("Do something completely unrelated"))

class RegistryTests(unittest.TestCase):
    def test_duplicate_rejected(self):
        registry = ToolRegistry()
        tool = registry.get("paypal_create_invoice")
        with self.assertRaises(ValueError):
            registry.register(tool)

if __name__ == "__main__":
    unittest.main()
