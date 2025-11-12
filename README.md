# Simple RAG Application

Simple implementation of RAG

## Tech

- __UI:__ Streamlit
- __API:__ FastAPI
- __LLM:__ OpenAI
- __Embedding:__ LangChain

## How to run:

__Terminal 1:__

``` bash
uvicorn app.server:app --reload --port 8000
```

__Terminal 2:__

``` bash
streamlit run ui/app.py
```
