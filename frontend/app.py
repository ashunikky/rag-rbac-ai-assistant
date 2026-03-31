import streamlit as st
import requests

st.title("🔐 RAG RBAC AI Assistant")

token = st.text_input("Enter JWT Token", type="password")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask something...")

if user_input and token:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        with st.spinner("Thinking... 🤔"):    
            response = requests.post(
                "https://rag-rbac-ai-assistant-backend.onrender.com//chat/stream",
                headers={"Authorization": f"Bearer {token}"},
                json={"query": user_input},
                stream=True
            )

            for chunk in response.iter_lines():
                if chunk:
                    text = chunk.decode("utf-8")
                    full_response += text + " "
                    placeholder.markdown(full_response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
    })