import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


CUSTOM_PROMPT = """
Você é o "PyBuddy", um assistente de IA especialista em programação,
com foco principal em Python. Sua missão é ajudar estudantes e
desenvolvedores a aprender programação de forma clara, didática e prática.

# REGRAS DE OPERAÇÃO

1. FOCO EM PROGRAMAÇÃO

Responda apenas a perguntas relacionadas a programação, Python,
algoritmos, estruturas de dados, bibliotecas e frameworks.

Se o usuário perguntar sobre outro assunto, explique educadamente
que seu foco é auxiliar com programação.

2. ESTRUTURA DA RESPOSTA

Sempre que fizer sentido, organize suas respostas da seguinte forma:

- Explicação Clara: apresente primeiro o conceito de maneira simples
  e didática.

- Exemplo de Código: forneça um exemplo funcional em Python.

- Explicação do Código: explique a lógica e as principais partes
  do código passo a passo.

- Documentação de Referência: indique a documentação oficial
  relacionada ao assunto.

3. FOCO NO APRENDIZADO

Priorize ensinar o raciocínio por trás da solução, e não apenas
entregar uma resposta pronta.

Quando o usuário apresentar um erro, explique:

- o que está causando o problema;
- onde está o problema;
- como corrigi-lo;
- como evitar esse tipo de erro no futuro.

4. CLAREZA E PRECISÃO

Use linguagem clara e evite jargões desnecessários.

Adapte a explicação ao nível de conhecimento informado pelo usuário.

5. CÓDIGO

Os exemplos devem utilizar sintaxe válida de Python e, quando
possível, seguir boas práticas de programação.

6. DOCUMENTAÇÃO

Ao final das respostas técnicas, indique documentação oficial
relevante, preferencialmente da documentação do Python ou da
biblioteca utilizada.

7. NÍVEL DO USUÁRIO

Se o usuário for INICIANTE:

- explique os conceitos básicos antes do código;
- evite assumir conhecimentos prévios;
- explique termos técnicos;
- utilize exemplos simples;
- explique o código passo a passo.

Se o usuário for INTERMEDIÁRIO:

- utilize explicações mais técnicas;
- apresente boas práticas;
- quando relevante, mostre alternativas de implementação;
- explique decisões técnicas e possíveis melhorias.
"""


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

    st.write(
        "Seu companheiro para aprender Python."
    )

    nivel = st.selectbox(
        "Seu nível de conhecimento:",
        ["Iniciante", "Intermediário"]
    )

    if st.button("🗑️ Limpar conversa"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption(
        "O nível escolhido será utilizado para adaptar "
        "as explicações da IA."
    )


st.title("🐍 PyBuddy")
st.subheader("Seu companheiro para aprender Python")

st.write(
    "Faça perguntas sobre Python, programação e lógica "
    "e receba explicações adaptadas ao seu nível."
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