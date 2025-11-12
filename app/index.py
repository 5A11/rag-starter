import os

from langchain_community.vectorstores import FAISS  # type: ignore
from langchain_openai import OpenAIEmbeddings

from .config import EMBEDDING_MODEL, INDEX_PATH, OPENAI_API_KEY


def get_embeddings():
    return OpenAIEmbeddings(model=EMBEDDING_MODEL, api_key=OPENAI_API_KEY)


def build_or_load_index(chunks):
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    embeddings = get_embeddings()
    if chunks:
        texts = [c["text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]
        vs = FAISS.from_texts(texts=texts, embedding=embeddings, metadatas=metadatas)
        vs.save_local(INDEX_PATH)
        return vs
    else:
        return FAISS.load_local(
            INDEX_PATH, embeddings, allow_dangerous_deserialization=True
        )
