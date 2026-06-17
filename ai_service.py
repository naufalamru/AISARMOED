import requests
import streamlit as st

try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
    st.success("API key ditemukan")
except Exception as e:
    st.error(str(e))

def ask_ai(prompt):

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "MMA AI Assistant"
    }

    data = {
        "model": "meta-llama/llama-3-8b-instruct",  # gratis / murah / stabil
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=data)

        # debug kalau error
        if response.status_code != 200:
            return f"⚠️ ERROR API: {response.text}"

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"⚠️ AI tidak tersedia: {str(e)}"
