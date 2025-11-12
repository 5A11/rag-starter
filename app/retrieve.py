from langchain_community.vectorstores import FAISS  # type: ignore

from .index import build_or_load_index


def retrieve(vs: FAISS, query, k=5):
    return vs.similarity_search(query, k=k)  # each: .page_content, .metadata
