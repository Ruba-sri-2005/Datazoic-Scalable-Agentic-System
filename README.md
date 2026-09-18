# Scalable Agentic System — Improved Assessment Prototype

This is an educational, runnable Python prototype for the Datazoic assessment. It demonstrates scalable tool discovery, routing, validation, session state, mock PayPal actions, a separate RAG tool, and a separate system-search tool.

**Scope:** The provided assessment describes a PayPal Postman collection with 50+ APIs, scaling toward 500+ APIs, but does not include the collection, API schemas, credentials, or required framework. This project therefore uses a realistic architecture and illustrative mock tools. It does not call PayPal or move money.

## Run
Python 3.10+; no external packages required.

```bash
python main.py
```

Run tests:
```bash
python -m unittest -v
```

## Example prompts
- `What tools are available for managing invoices?`
- `How do I create an invoice?`
- `Create an invoice for $50 to alex@example.com`
- `Is there an open dispute from user_123?`
- `What was my total sales volume last month?`
- `What is the status of my last request?`

The invoice action is a **mock**. Payment execution is deliberately disabled.

## Contents
- `agent.py`: request classification, candidate retrieval, state, clarification, execution.
- `tool_registry.py`: tool metadata, indexed discovery, argument validation, mock adapters.
- `knowledge.py`: separate documentation retrieval tool.
- `system_search.py`: separate tool catalog and session-history search.
- `tests/`: automated unit tests.
- `docs/architecture.md`: architecture, scaling plan, framework trade-offs, safety and observability.
- `docs/interview_notes.md`: short oral explanation and likely questions.

## Production work still required
Import the actual Postman collection; generate validated schemas; implement authenticated provider adapters; use hybrid retrieval/reranking; persist state; add robust retries, tracing, authorization, rate limits, and sandbox tests.
