import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# 🔹 Standard response
def generate_llm_response(query, context, chat_history=None):
    try:
        history_text = ""
        if chat_history:
            history_text = "\n".join(chat_history)

        prompt = f"""
You are a company assistant with strict access control.

Rules:
- Answer ONLY from the provided context
- Do NOT make up information
- If answer not found, say: "No relevant data found for your role"
- Be clear and professional

Conversation History:
{history_text}

Context:
{context}

User Query:
{query}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a secure enterprise assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating response: {str(e)}"


# 🔥 Streaming response (optional advanced feature)
def generate_streaming_response(query, context):
    try:
        prompt = f"""
Answer ONLY from context.

Context:
{context}

Query:
{query}
"""

        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )

        for chunk in stream:
            yield chunk.choices[0].delta.content or ""

    except Exception as e:
        yield f"Error: {str(e)}"