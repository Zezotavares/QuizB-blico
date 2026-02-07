import streamlit as st
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Jornada Bíblica Cinematográfica", page_icon="📖", layout="wide")

# --- ESTILO VISUAL CINEMATOGRÁFICO (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e0e0e;
        color: #e0c097;
    }
    
    .titulo-abertura {
        font-family: 'Georgia', serif;
        color: #ffca28;
        text-align: center;
        font-size: 4rem;
        font-weight: bold;
        text-shadow: 0px 0px 20px rgba(255, 202, 40, 0.5);
        margin-bottom: 20px;
    }

    div.stButton > button:first-child {
        background: linear-gradient(180deg, #d4af37 0%, #aa841e 100%);
        color: #000 !important;
        font-size: 24px;
        font-weight: bold;
        border-radius: 50px;
        border: 2px solid #ffca28;
        padding: 15px 50px;
        width: 300px;
        display: block;
        margin: 0 auto;
        transition: 0.5s;
    }

    div.stButton > button:first-child:hover {
        box-shadow: 0px 0px 30px #ffca28;
        transform: scale(1.1);
    }

    .referencia-container {
        background-color: rgba(255, 255, 255, 0.1);
        border-left: 10px solid #d4af37;
        padding: 20px;
        border-radius: 5px;
        margin-top: 25px;
    }

    .referencia-texto {
        font-size: 22px;
        color: #ffca28;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO ESTADO ---
if 'jogo_iniciado' not in st.session_state:
    st.session_state.jogo_iniciado = False
if 'pontuacao' not in st.session_state:
    st.session_state.pontuacao = 0
if 'sessao_atual' not in st.session_state:
    st.session_state.sessao_atual = 1
if 'pergunta_indice' not in st.session_state:
    st.session_state.pergunta_indice = 0

# --- BANCO DE DADOS ---
sessoes_historia = {
    1: {
        "titulo": "Sessão 1: As Origens",
        "perguntas": [
            {
                "pergunta": "No princípio, o que pairava sobre a face das águas?",
                "opcoes": ["A) O Espírito de Deus", "B) Uma grande nuvem", "C) O Sol e a Lua", "D) Nada"],
                "resposta": "A",
                "referencia": "Gênesis 1:2",
                "video": "criacao.mp4"
            }
        ]
    }
}

# --- TELAS ---

def mostrar_tela_abertura():
    st.markdown("<h1 class='titulo-abertura'>JORNADA BÍBLICA<br>CINEMATOGRÁFICA</h1>", unsafe_allow_html=True)
    
    # Vídeo de abertura SEM LOOP
    try:
        with open("abertura.mp4", 'rb') as video_file:
            # loop=False garante que ele toque apenas uma vez
            st.video(video_file.read(), loop=False, autoplay=True)
    except FileNotFoundError:
        st.error("Arquivo 'abertura.mp4' não encontrado na pasta do projeto.")

    st.write("<br>", unsafe_allow_html=True)
    
    if st.button("INICIAR JORNADA"):
        st.session_state.jogo_iniciado = True
        st.rerun()

def mostrar_quiz():
    sessao = sessoes_historia[st.session_state.sessao_atual]
    item = sessao["perguntas"][st.session_state.pergunta_indice]

    st.markdown(f"## {sessao['titulo']}")
    
    try:
        with open(item['video'], 'rb') as video_p:
            # Vídeos das perguntas também sem loop para manter a consistência
            st.video(video_p.read(), loop=False, autoplay=True)
    except FileNotFoundError:
        st.warning(f"Vídeo {item['video']} não encontrado.")

    st.markdown(f"### {item['pergunta']}")

    cols = st.columns(2)
    for i, opcao in enumerate(item['opcoes']):
        with cols[i % 2]:
            if st.button(opcao, key=f"btn_{i}"):
                if opcao[0] == item['resposta']:
                    st.balloons()
                    st.success("✔ EXCELENTE!")
                    st.markdown(f"<div class='referencia-container'><span class='referencia-texto'>📖 Onde diz na Bíblia: {item['referencia']}</span></div>", unsafe_allow_html=True)
                    st.session_state.pontuacao += 1
                    time.sleep(5)
                else:
                    st.error(f"✘ INCORRETO. A resposta era {item['resposta']}.")
                    time.sleep(3)
                
                # Avançar lógica
                if st.session_state.pergunta_indice < len(sessao["perguntas"]) - 1:
                    st.session_state.pergunta_indice += 1
                else:
                    st.session_state.sessao_atual += 1
                    st.session_state.pergunta_indice = 0
                st.rerun()

# --- EXECUÇÃO ---
if not st.session_state.jogo_iniciado:
    mostrar_tela_abertura()
else:
    if st.session_state.sessao_atual in sessoes_historia:
        mostrar_quiz()
    else:
        st.title("🏆 Jornada Concluída!")
        if st.button("Reiniciar"):
            st.session_state.jogo_iniciado = False
            st.session_state.pontuacao = 0
            st.session_state.sessao_atual = 1
            st.session_state.pergunta_indice = 0
            st.rerun()