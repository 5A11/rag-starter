## Make it reliable (first upgrades)

1. Chunking strategy
  - Start: RecursiveCharacterTextSplitter(800/120)
  - Upgrade: Markdown/HTML-aware splitters; keep headings in metadata.

2. Hybrid retrieval
  - Add a keyword retriever (BM25) and mix with vector hits: rerank top-k.

3. Prompting
  - Keep temperature ≤ 0.3.
  - Force “if not in context, say ‘I don’t know’”.

4. Citations
  - Always include N snippets with source + page/URL.
  - Show these snippets in the UI under the answer for trust.

5. Guardrails
  - Add max context tokens; drop low-similarity chunks.
  - Add banned content filters if needed.

## Deployment path (when you’re ready)

- Internal demo: Dockerise FastAPI + Streamlit, run on Fly.io/Render.
- API only: Expose /ask behind FastAPI, add simple API key.
- Observability: Log queries, latency, source doc IDs, similarity scores; add a CSV/SQLite sink first.
- Privacy: Strip PII at ingestion (regex or Presidio) if using sensitive docs.

## Productisation angles (choose one to lean into)

- Enterprise knowledge assistant (SSO, role-based corpora, analytics)
- Regulatory copilot (RAG over policy + audit trail of citations)
- Support copilot (RAG over past tickets + macro suggestions)
- Sales enablement (RAG over battlecards + CRM notes + pricing)

## Week-1 sprint plan (very concrete)

__Day 1–2__
- Scaffold repo, install deps, wire .env, run local Stack.
- Ingest 1 PDF + 1 URL; confirm retrieval; ask 5 sample questions.

__Day 3__
- Add citations & UI display; enforce “I don’t know” logic.
- Build tiny eval set (10 Q/A) from your documents.

__Day 4__
- Add RAGAS; measure faithfulness & relevancy; tweak chunk size / top-k.

__Day 5__
- Add hybrid retrieval (BM25 + vectors) and re-run eval.
- Write a one-pager: problem → approach → metrics → demo link.

Deliverables by the end of the week:
- Running app (API + UI)
- 10-question eval with scores
- Short demo video (2–3 min, Loom)

## Optional “local-only” variant (no external APIs)

- Install Ollama; set EMBEDDING_MODEL=local-nomic (wrap call) and LLM_MODEL=llama3.1:8b.
- Swap OpenAIEmbeddings for a local embedding call (store vectors via chromadb or faiss).
- Pros: privacy, zero cost; Cons: lower quality, more tuning.

## Next best improvements (after MVP works)

- Re-ranking with a cross-encoder (e.g., bge-reranker) to boost citation quality.
- Section-aware retrieval: attach heading tree; collapse near-duplicate chunks.
- Query reformulation: HyDE / multi-query expansion for recall.
- Caching: exact-match + semantic cache (sqlite or Redis) to cut latency/cost.
- Multi-tenant: namespace indexes per user/org; quotas.