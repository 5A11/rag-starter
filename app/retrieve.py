from langchain_community.vectorstores import FAISS  # type: ignore


def retrieve(vs: FAISS, query, k=5, with_scores=True):
    if with_scores and hasattr(vs, "similarity_search_with_score"):
        return vs.similarity_search_with_score(query, k=k)  # [(doc, score), ...]
    else:
        docs = vs.similarity_search(query, k=k)
        return [(d, None) for d in docs]
