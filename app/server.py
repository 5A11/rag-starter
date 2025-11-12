import os
import tempfile

from fastapi import FastAPI, Form, UploadFile

from .generate import answer
from .index import build_or_load_index
from .ingest import chunk_docs, load_pdf, load_url

app = FastAPI()
_vs = None


@app.post("/ingest_pdf")
async def ingest_pdf(file: UploadFile):
    global _vs
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp.flush()
        docs = list(load_pdf(tmp.name))
    chunks = chunk_docs(docs)
    _vs = build_or_load_index(chunks)
    return {"chunks": len(chunks)}


@app.post("/ingest_url")
async def ingest_url(url: str = Form(...)):
    global _vs
    docs = load_url(url)
    chunks = chunk_docs(docs)
    _vs = build_or_load_index(chunks)
    return {"chunks": len(chunks)}


@app.get("/ask")
async def ask(q: str):
    global _vs
    if not _vs:
        _vs = build_or_load_index(chunks=None)
    ans, docs = answer(_vs, q)
    cites = [{"i": i + 1, "meta": d.metadata} for i, d in enumerate(docs)]
    return {"answer": ans, "citations": cites}
