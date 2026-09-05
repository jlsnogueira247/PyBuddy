import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="PyBuddy",
    page_icon="🐍",
    layout="wide"
)

# Título principal
st.title("🐍 PyBuddy")

st.subheader("Seu companheiro para aprender Python")

st.write(
    "Faça perguntas sobre Python, programação e lógica "
    "e receba explicações simples com exemplos de código."
)

# Campo para pergunta
pergunta = st.chat_input("Digite sua dúvida sobre Python...")

# Exibe a pergunta do usuário
if pergunta:
    st.write("Sua pergunta:")
    st.write(pergunta)