import requests
import streamlit as st

def generate_with_groq(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {st.secrets['groq_api_key']}",
        "Content-Type": "application/json"
    }

    data = {
    "model": "llama-3.3-70b-versatile",  # Alternatif: "mistral-saba-24b"
    "messages": [
        {"role": "system", "content": "Sen deneyimli bir içerik uzmanısın."},
        {"role": "user", "content": prompt}
    ]
}


    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=data
    )

    if response.status_code != 200:
        raise Exception(f"Hata kodu: {response.status_code} - {response.text}")

    return response.json()["choices"][0]["message"]["content"].strip()
