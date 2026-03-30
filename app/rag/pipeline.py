from app.db.vectorstore import get_vectorstore
from app.llm.groq_client import generate_llm_response
from app.rag.retriever import get_retriever

def retrieve_docs(query, role):
    retriever = get_retriever(role)

    docs = retriever.invoke(query)

    filtered_docs = []

    for d in docs:
        if role in d.metadata.get("access_roles", []):
            filtered_docs.append(d)

    return [
        {
            "text": d.page_content,
            "metadata": d.metadata
        }
        for d in filtered_docs
    ]

def generate_answer(query, docs):
    if not docs:
        return "No relevant data found."

    context = "\n".join([d["text"] for d in docs])

    return generate_llm_response(query, context)

def rag_pipeline(query, role, chat_history=[]):
    docs = retrieve_docs(query, role)

    context = "\n".join([d["text"] for d in docs])

    history_text = "\n".join(chat_history)

    final_prompt = f"""
Conversation History:
{history_text}

Context:
{context}

User Query:
{query}
"""

    answer = generate_llm_response(query, final_prompt)

    return {
        "answer": answer,
        "sources": [d["metadata"] for d in docs]
    }