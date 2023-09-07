import os

import pinecone
import streamlit as st
from langchain import GoogleSearchAPIWrapper
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores import Pinecone
from langchain.vectorstores.base import VectorStoreRetriever

from utils.constants import CHARACTERS

search = GoogleSearchAPIWrapper(k=6)


@st.cache_resource(show_spinner=False)
def get_retrievers() -> dict:  # to get vector_stores
    pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV"))
    indexes = pinecone.list_indexes()

    retrievers = {}
    for name in CHARACTERS:
        index_name = name.replace(" ", "-").lower()
        if index_name not in indexes:
            pinecone.create_index(name=index_name, metric='cosine', dimension=1536)
        retrievers[name] = Pinecone.from_existing_index(
            index_name=index_name,
            embedding=OpenAIEmbeddings()
        ).as_retriever(k=5)
    return retrievers


@st.cache_resource(show_spinner=False)
def get_retriever() -> VectorStoreRetriever:
    pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV"))
    indexes = pinecone.list_indexes()
    if "naija-echoes" not in indexes:
        pinecone.create_index(name="naija-echoes", metric='cosine', dimension=1536)
    return Pinecone.from_existing_index(
        index_name="naija-echoes",
        embedding=OpenAIEmbeddings()
    ).as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.85})


@st.cache_resource(ttl=10800, show_spinner=False)
def get_latest_news() -> dict:
    results = {}
    for name in CHARACTERS:
        if name not in results.keys():
            results[name] = search.run(f"latest on {name}")
    return results


async def get_relevant_info(hero_name: str, query: str) -> str:
    # docs = get_retrievers()[hero_name].aget_relevant_documents(query=query)
    query = f"{hero_name} {query}"
    docs = await get_retriever().aget_relevant_documents(query=query, k=6)
    if len(docs) < 2:
        search_result = search.run(query=query)
        get_retriever().add_documents([Document(page_content=f"{hero_name}\n\n{search_result}")])
        return search_result
    else:
        return "\n".join([doc.page_content for doc in docs])
