import os

import requests  # type: ignore
import streamlit as st

API = os.getenv("API_URL", "http://127.0.0.1:8000")

st.title("RAG Starter")
with st.sidebar:
    st.header("Ingest")
    pdf = st.file_uploader("Upload PDF", type=["pdf"])
    if pdf and st.button("Index PDF"):
        r = requests.post(f"{API}/ingest_pdf", files={"file": pdf.getvalue()})
        st.success(r.json())

    url = st.text_input("URL")
    if st.button("Index URL") and url:
        r = requests.post(f"{API}/ingest_url", data={"url": url})
        st.success(r.json())

q = st.text_input("Ask a question")
if st.button("Ask") and q:
    r = requests.get(f"{API}/ask", params={"q": q}).json()
    st.subheader("Answer")
    st.write(r["answer"])
    st.subheader("Citations")
    for c in r["citations"]:
        st.caption(f"{c['meta']}  |  score={c['score']}")
