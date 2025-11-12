import fitz  # type: ignore
import httpx
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from readability import Document  # type: ignore

from .config import CHUNK_OVERLAP, CHUNK_SIZE


def load_pdf(path):
    doc = fitz.open(path)
    for i, page in enumerate(doc):
        text = page.get_text("text")
        yield {"text": text, "metadata": {"source": path, "page": i + 1}}


def load_url(url):
    html = httpx.get(url, timeout=30).text
    doc = Document(html)
    content = BeautifulSoup(doc.summary(), "html.parser").get_text(" ", strip=True)
    title = doc.short_title() or url
    return [{"text": content, "metadata": {"source": url, "title": title}}]


def chunk_docs(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", ".", " "],
    )
    chunks = []
    for d in documents:
        for chunk in splitter.split_text(d["text"]):
            meta = dict(d["metadata"])
            meta["len"] = len(chunk)
            chunks.append({"text": chunk, "metadata": meta})
    return chunks
