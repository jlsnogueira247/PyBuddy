import streamlit as st
from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)

# Configuração da página
st.set_page_config(
    page_title="PyBuddy",
    page_icon="🐍",
    layout="wide"
)

st.title("🐍 PyBuddy")

st.subheader("Seu companheiro para aprender Python")

st.write(
    "Faça perguntas sobre Python, programação e lógica "
    "e receba explicações simples com exemplos de código."
)

pergunta = st.chat_input("Digite sua dúvida sobre Python...")

if pergunta:
    st.write("Sua pergunta:")
    st.write(pergunta)

    resposta = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": pergunta
            }
        ],
        temperature=0.7,
        max_tokens=2048
    )

    st.write(resposta.choices[0].message.content)