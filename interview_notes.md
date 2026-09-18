# Interview Notes

## 60-second explanation
“My system does not expose hundreds of tool definitions to the LLM at once. Each tool is stored in a registry with its description, category, parameters, and permission metadata. The router retrieves a small candidate set, checks required arguments, and asks for clarification instead of guessing. A provider adapter executes the selected API. RAG and System Search are separate tools. I also track session state and request history. For production, I would add hybrid retrieval, schema validation, authentication, confirmation for side effects, idempotency, retries, and LangSmith tracing. This prototype uses mock APIs because the provided PDF does not include the real PayPal collection or credentials.”

## Questions to practice
**Why not give all tools to the model?** It increases irrelevant choices, context size, and the risk of wrong selection. Retrieval narrows candidates.

**How scale to 1,000 tools?** Index tool metadata; filter by service/category/permissions; hybrid-search and rerank; pass only top-k; monitor routing quality.

**What if parameters are missing?** Validate and ask the user. Never invent amounts, recipient IDs, or dates.

**How protect payments?** Authentication, authorization, preview, explicit confirmation, idempotency key, audit log, and provider-response verification.

**What does RAG do?** Searches approved documents and returns relevant evidence for grounded answers.

**What does System Search do?** Searches tool capabilities or the authenticated user's request history.

**Why LangGraph?** Explicit state and conditional workflow routing; trade-off is additional complexity.

**What is implemented vs proposed?** Implemented: small mock registry, lexical discovery, routing, basic validation, RAG-style retrieval, system search, session history, and tests. Proposed: real API adapters, OAuth, vector/hybrid retrieval, persistent state, LangGraph, LangSmith, production retries and deployment.
