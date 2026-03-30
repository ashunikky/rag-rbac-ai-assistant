from app.db.vectorstore import get_vectorstore

def get_retriever(user_role):
    vectordb = get_vectorstore()

    retriever = vectordb.as_retriever(
        search_kwargs={
            "k": 5,
            
        }
    )

    return retriever

def test_retriever():
    vectordb = get_vectorstore()

    docs = vectordb.get()

    print("Total stored docs:", len(docs["documents"]))

    for i, doc in enumerate(docs["documents"]):
        print("\n---")
        print("TEXT:", doc)