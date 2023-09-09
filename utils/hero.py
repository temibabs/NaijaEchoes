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


def get_relevant_info(hero_name: str, query: str) -> str:
    # docs = get_retrievers()[hero_name].aget_relevant_documents(query=query)
    query = f"{hero_name} {query}"
    docs = get_retriever().get_relevant_documents(query=query, k=6)
    if len(docs) < 2:
        search_result = search.run(query=query)
        get_retriever().add_documents([Document(page_content=f"{hero_name}\n\n{search_result}")])
        return search_result
    else:
        return "\n".join([doc.page_content for doc in docs])


@st.cache_resource
def get_sample_speeches():
    return {
        "Bola Ahmed Tinubu": """The defects in our economy immensely profited a tiny elite, the elite of the elite you might call them. 
As we move to fight the flaws in the economy, the people who grow rich from them, predictably, will fight back through every means necessary... But I urge you all to look beyond the present temporary pains and aim at the larger picture. 
All of our good and helpful plans are in the works. More importantly, I know that they will work... We are exiting the darkness to enter a new and glorious dawn.""",
        "Buchi Emecheta": """Writers simply have to write, and not worry so much about what people think, because public opinion is such a difficult horse to ride.""",
        "Burna Boy": """Apparently, City Boy = A city dweller with sophisticated manners and clothing   🤷🏾‍♂️🤨""",
        "Chimamanda Adichie": """I can’t believe it’s been ten years since AMERICANAH went out into the world. 
I wrote a new introduction for the 10TH ANNIVERSARY SPECIAL EDITION, which is out today!
Thank you to my wonderful publishers @4thEstateBooks and @AAKnopf""",
        "Chinua Achebe": """When a man is at peace with his gods and ancestors, his harvest will be good or bad according to the strength of his arm""",
        "Davido": """Crème De La Crème. Shutting down DXB tomorrow 🇦🇪⏳ See you soon !
Shey make them ban money ? Na money Dey cause problem 😂😂""",
        "Don Jazzy": """So if I say make you give me your girlfriend you no go give me?
Unveiling a new artist is a reminder of how an artist have let themselves go through the laid down process of the Mavin academy, the testament of our faith in them and the coming together of our hardwork.
With the power vested in me by the Supreme Mavin Dynasty It’s my pleasure to introduce you to Mavin’s latest signee.""",
        "Ezra Olubi": """you can tell the food is hitting when you see me take off my glasses 🌶️
i might have to sign up for ads revenue sharing so i can make some money off people's enmity with comprehension""",
        "Iyin Aboyeji": """Everyone is entitled to his own opinion, but not his own facts. I specifically remember what you said to 
@BWLawal and then what you said yesterday again. Just stop the sanctimonious behavior. Nobody holy pass.""",
        "Odun Eweniyi": """older people do love to stand on existing protocol and then add their own what hell is this
this parallel is exactly why i will still argue 🙏🏾 - love how everyone is glued to this thing but deep deep deep down you know nothing changes.""",
        "Peter Obi": """Today at Arochukwu, Abia State, I joined the Ohuabunwa family, notable political and business leaders, and other respected Nigerians for the funeral church service of Lady Nimi Faith Ohuabunwa, wife of Senator Mao Ohuabunwa.""",
        "Wizkid": """London Next July 29th See you soon! ❤️
No family is perfect, we argue, we fight, we even stop talking to each other at times but in the end, the family is family… the love will always be there.""",
        "Wole Soyinka": """Books and all forms of writing are terror to those who wish to suppress the truth.
But theater, because of its nature, both text, images, multimedia effects, has a wider base of communication with an audience. That's why I call it the most social of the various art forms.""",
        "Yele Bademosi": """We essentially created something similar to Uber, DoorDash or Airbnb for on/off ramps
Grateful to continue the journey with my incredible Co-founder 
@logbon72 and we want to take a moment to express our gratitude to each and every Nester for their unwavering commitment and the incredible hard work they’ve put in the last 11 months.""",
    }
