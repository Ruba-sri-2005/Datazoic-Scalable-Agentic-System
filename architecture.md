# Architecture and Design Rationale

## Problem statement
The assessment asks for an agent that can work with a PayPal Postman collection containing 50+ API calls and scale toward 500+ APIs across services. The core concern is wrong tool selection, hallucinated parameters, and task failure as choices grow.

## Proposed request lifecycle
1. Receive the user request and authenticated session context.
2. Classify it as an action, a documentation question (RAG), or a system/catalog query.
3. Retrieve a small candidate set from the tool registry using metadata search.
4. Ask a clarification question if intent or required arguments are missing.
5. Validate arguments against the selected tool's schema.
6. Apply permissions and explicit confirmation gates to side-effecting actions.
7. Execute through a provider adapter; normalize success/error results.
8. Store state and sanitized request telemetry; answer only from confirmed results.

## Tool registry and scaling
Store each tool's stable name, description, service, category, required/optional parameters, JSON Schema/OpenAPI schema, permission scope, side-effect classification, and adapter reference. For production, use lexical + embedding (hybrid) retrieval, metadata filters, and reranking. Supply only top-k candidates to the LLM. This reduces irrelevant choices and context load. The included prototype uses simple lexical overlap only.

## Agent and state
Use a central orchestrator with explicit states: received, classified, candidates_retrieved, awaiting_clarification, validated, awaiting_confirmation, executing, succeeded, failed. Persist session/request state in PostgreSQL or Redis in production. Use idempotency keys for retried writes.

## RAG tool
Keep RAG as a separate tool. Retrieve approved documentation passages, return source metadata, and ground explanatory answers in those passages. If retrieval has no evidence, say so rather than inventing details.

## System Search tool
Keep system search separate. It can search tool capabilities and request status/history. In production, enforce user/session access controls and redact secrets and sensitive fields.

## Error handling and safety
- Missing or malformed fields: ask the user; never guess identifiers or amounts.
- Provider 429/timeouts: bounded exponential backoff with jitter; honor Retry-After.
- Retry only safe/idempotent operations or writes protected by idempotency keys.
- Side effects: authenticate, authorize, preview, require explicit confirmation, log audit event.
- Never claim success until the provider confirms it.
- Return concise actionable errors; redact tokens and personal data from logs.

## Framework choice and trade-offs
**Production proposal: LangGraph** for explicit stateful orchestration and conditional routing. It makes workflow state and branching visible, but adds learning and operational complexity.

**LangChain:** broad integrations and fast prototyping; however, simply registering many tools does not solve retrieval/routing ambiguity, so a registry and validation layer are still needed.

**LlamaIndex:** strong fit for document ingestion and RAG; it does not replace the action execution, authorization, and transaction-safety layer.

**CrewAI:** useful for role-based multi-agent workflows; multiple agents can add latency and coordination overhead when one orchestrated route is sufficient.

**From scratch:** maximum control and fewer dependencies, but state, retries, tracing, and integrations must be built and maintained.

The prototype uses standard-library Python so it can run without keys or dependencies. That is a demonstrator, not the recommended production stack.

## Observability
Use LangSmith or equivalent tracing for request ID, classification, candidate tools, chosen tool, validation, latency, retries, and sanitized outcome. Track routing accuracy, completion rate, clarification rate, tool error rate, latency, and cost.

## Limits and assumptions
The supplied PDF does not contain the actual Postman collection, full API schemas, credentials, or mandatory framework. Therefore, this project demonstrates the design with mock tools. Production completion requires importing the real collection, implementing provider adapters/OAuth, and testing against a sandbox.
