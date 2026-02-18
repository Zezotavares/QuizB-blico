import streamlit as st
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Jornada Bíblica Cinematográfica", page_icon="📖", layout="wide")

# --- ESTILO VISUAL CINEMATOGRÁFICO (CSS) ---
st.markdown("""
    <style>
    /* Fundo escuro profundo */
    .stApp {
        background-color: #000000;
        color: #e0c097;
    }
    
    /* ESCONDER CONTROLES DO VÍDEO (Pausa, Tempo, Som) */
    video::-webkit-media-controls {
        display:none !important;
    }
    video::-webkit-media-controls-enclosure {
        display:none !important;
    }
    video {
        width: 100vw;
        height: auto;
        object-fit: cover;
        border-radius: 0px;
        pointer-events: none; /* Impede que o usuário pause ao clicar no vídeo */
    }

    /* Centralizar título da abertura */
    .titulo-abertura {
        font-family: 'Georgia', serif;
        color: #ffca28;
        text-align: center;
        font-size: 4rem;
        font-weight: bold;
        text-shadow: 0px 0px 20px rgba(255, 202, 40, 0.5);
        margin-bottom: 10px;
    }

    /* Estilização do Botão Iniciar */
    div.stButton > button:first-child {
        background: linear-gradient(180deg, #d4af37 0%, #aa841e 100%);
        color: #000 !important;
        font-size: 24px;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        padding: 15px 50px;
        width: 350px;
        display: block;
        margin: 0 auto;
        transition: 0.5s;
    }

    div.stButton > button:first-child:hover {
        box-shadow: 0px 0px 40px #ffca28;
        transform: scale(1.05);
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

# --- BANCO DE DADOS (Exemplo com 1 pergunta) ---
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
    st.markdown("<h1 class='titulo-abertura'>JORNADA BÍBLICA</h1>", unsafe_allow_html=True)
    
    try:
        with open("abertura.mp4", 'rb') as f:
            # autoplay=True e loop=False conforme solicitado
            st.video(f.read(), autoplay=True, loop=False)
    except FileNotFoundError:
        st.error("Certifique-se de que o vídeo 'abertura.mp4' está na mesma pasta que este código.")

    st.write("<br>", unsafe_allow_html=True)
    
    if st.button("INICIAR JORNADA"):
        st.session_state.jogo_iniciado = True
        st.rerun()

def mostrar_quiz():
    sessao = sessoes_historia[st.session_state.sessao_atual]
    item = sessao["perguntas"][st.session_state.pergunta_indice]

    try:
        with open(item['video'], 'rb') as f:
            st.video(f.read(), autoplay=True, loop=False)
    except FileNotFoundError:
        st.warning(f"Vídeo {item['video']} não encontrado.")

    st.markdown(f"### {item['pergunta']}")

    cols = st.columns(2)
    for i, opcao in enumerate(item['opcoes']):
        with cols[i % 2]:
            if st.button(opcao):
                if opcao[0] == item['resposta']:
                    st.success(f"✨ Correto! {item['referencia']}")
                    st.session_state.pontuacao += 1
                    time.sleep(3)
                else:
                    st.error(f"✘ Errado. A resposta era {item['resposta']}.")
                    time.sleep(2)
                
                # Avançar
                st.session_state.pergunta_indice = 0 # Ajuste conforme crescer o banco
                st.session_state.sessao_atual += 1
                st.rerun()

# --- EXECUÇÃO ---
if not st.session_state.jogo_iniciado:
    mostrar_tela_abertura()
else:
    if st.session_state.sessao_atual in sessoes_historia:
        mostrar_quiz()
    else:
        st.title("Fim da Jornada!")
        if st.button("Reiniciar"):
            st.session_state.jogo_iniciado = False
            st.rerun()