from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

embedding = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

def get_vectorstore():
    vectordb = Chroma(
        collection_name="company_data",
        embedding_function=embedding,
        persist_directory="./db"
    )
    return vectordb