import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from prompts import CUSTOM_PROMPT

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="PyBuddy",
    page_icon="🐍",
    layout="wide"
)


if not groq_api_key:
    st.error("API Key da Groq não encontrada.")
    st.stop()


client = Groq(api_key=groq_api_key)


if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
    st.title("🐍 PyBuddy")

    st.caption("Seu companheiro para aprender Python.")

    st.divider()

    st.subheader("🎓 Seu nível")

    nivel = st.selectbox(
        "Escolha seu nível de conhecimento:",
        ["Iniciante", "Intermediário"]
    )

    st.caption(
        "O nível escolhido será utilizado para adaptar "
        "as explicações da IA."
    )

    st.divider()

    if st.button("🗑️ Limpar conversa", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.subheader("ℹ️ Sobre")

    st.write(
        "O PyBuddy é um assistente de programação desenvolvido "
        "em Python para auxiliar no aprendizado de programação."
    )


st.title("🐍 PyBuddy")

st.subheader("Seu companheiro para aprender Python")

st.write(
    "Tire suas dúvidas, entenda seus erros e aprenda "
    "programação na prática."
)

st.divider()

if not st.session_state.messages:
    st.info(
        "👋 Olá! Eu sou o PyBuddy. "
        "Faça uma pergunta sobre Python, programação ou lógica "
        "para começarmos."
    )   


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


pergunta = st.chat_input(
    "Digite sua dúvida sobre Python..."
)

if pergunta:

    with st.chat_message("user"):
        st.markdown(pergunta)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": pergunta
        }
    )

    prompt_com_nivel = CUSTOM_PROMPT + f"""

O nível de conhecimento informado pelo usuário é: {nivel}.

Adapte sua resposta de acordo com esse nível.
"""

    try:

        resposta = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": prompt_com_nivel
                },
                *st.session_state.messages
            ],
            temperature=0.7,
            max_tokens=2048
        )

        conteudo_resposta = resposta.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(conteudo_resposta)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": conteudo_resposta
            }
        )

    except Exception:
        st.error(
        "⚠️ Não foi possível obter uma resposta. "
        "Verifique sua conexão ou tente novamente."
        )