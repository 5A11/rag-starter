from openai import OpenAI

from .config import LLM_MODEL, OPENAI_API_KEY, TOP_K
from .retrieve import retrieve

client = OpenAI(api_key=OPENAI_API_KEY)

PROMPT = """You are a careful assistant. Use ONLY the provided context to answer.
If the answer is not in the context, say you don't know.
Cite sources as [#] with their page/URL.

Question: {q}

Context:
{ctx}
"""


def format_ctx(docs):
    lines = []
    for i, d in enumerate(docs, start=1):
        src = d.metadata.get("title") or d.metadata.get("source")
        page = d.metadata.get("page")
        tag = f"{src}"
        if page:
            tag += f" p.{page}"
        lines.append(f"[{i}] {tag}\n{d.page_content[:1200]}")
    return "\n\n".join(lines)


def answer(vs, query):
    docs = retrieve(vs, query, k=TOP_K)
    ctx = format_ctx(docs)
    msg = PROMPT.format(q=query, ctx=ctx)
    resp = client.chat.completions.create(
        model=LLM_MODEL, messages=[{"role": "user", "content": msg}], temperature=0.2
    )
    return resp.choices[0].message.content, docs
