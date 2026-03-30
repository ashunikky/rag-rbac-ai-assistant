import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.db.vectorstore import get_vectorstore

def load_documents(data_path, department):
    docs = []

    for file in os.listdir(data_path):
        if file.endswith(".txt"):
            loader = TextLoader(os.path.join(data_path, file))
            loaded_docs = loader.load()

            for doc in loaded_docs:
                doc.metadata["department"] = department
                doc.metadata["access_roles"] = [department, "c_level"]

                # General is accessible to everyone
                if department == "general":
                    doc.metadata["access_roles"] = [
                        "employee", "finance", "marketing",
                        "hr", "engineering", "c_level"
                    ]

            docs.extend(loaded_docs)

    return docs


def get_all_documents():
    base_path = "data"

    all_docs = []

    departments = ["finance", "hr", "marketing", "engineering", "general"]

    for dept in departments:
        path = os.path.join(base_path, dept)
        all_docs.extend(load_documents(path, dept))

    return all_docs

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return splitter.split_documents(documents)

def ingest_data():
    docs = get_all_documents()
    print("Total docs loaded:", len(docs))

    split_docs = split_documents(docs)
    print("Total chunks:", len(split_docs))

    vectordb = get_vectorstore()
    vectordb.add_documents(split_docs)

    print("✅ Data ingestion complete")

if __name__ == "__main__":
    ingest_data()