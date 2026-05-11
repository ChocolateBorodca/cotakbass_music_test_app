import streamlit as st
import os

st.set_page_config(page_title="cotakbass music", layout="wide", initial_sidebar_state="collapsed")

# УЛЬТРА-ФИКС: Прячем стандартные загрузчики и наводим матовое стекло
st.markdown(f"""
    <style>
    header, footer, #MainMenu, [data-testid="stInputInstructions"] {{ visibility: hidden !important; }}
    .stApp {{ background-color: #000000; color: #FFFFFF; font-family: -apple-system, sans-serif; }}

    /* Название приложения */
    .main-title {{
        font-size: clamp(32px, 8vw, 54px); font-weight: 800; letter-spacing: -2px;
        text-align: center; color: #FFFFFF;
        margin-bottom: 50px; margin-top: 20px;
    }}

    /* Прячем стандартный вид загрузчика файлов */
    div[data-testid="stFileUploader"] section {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }}
    div[data-testid="stFileUploader"] section > div {{ display: none !important; }}
    div[data-testid="stFileUploader"] {{ margin-bottom: -50px; }}

    /* Стеклянный прямоугольник (ФОН) */
    .glass-bg {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        height: 180px; width: 100%; max-width: 600px;
        margin: 0 auto;
        cursor: pointer;
    }}

    /* Круглая аватарка (ЦЕНТР) */
    .avatar-frame {{
        width: 140px; height: 140px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(30px);
        border: 2px solid #A020F0;
        border-radius: 50%;
        margin: -70px auto 40px auto;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 0 20px rgba(160, 32, 240, 0.2);
    }}

    /* Стеклянные инпуты */
    div[data-testid="stTextInput"] div[data-baseweb="input"] {{
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 15px !important;
        color: white !important;
    }}
    div[data-testid="stTextInput"] input {{ text-align: center !important; }}
    div[data-testid="stTextInput"] label {{ display: none !important; }}

    /* Кнопка ДВЕРЬ (Вход) */
    .login-btn-container {{ text-align: center; margin-top: 30px; }}
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(40px) !important;
        border: 1px solid rgba(160, 32, 240, 0.5) !important;
        border-radius: 50% !important;
        color: #A020F0 !important;
        width: 80px !important; height: 80px !important;
        font-size: 30px !important;
        transition: 0.4s !important;
    }}
    div.stButton > button:hover {{
        box-shadow: 0 0 30px rgba(160, 32, 240, 0.4);
        transform: scale(1.1);
    }}
    </style>
""", unsafe_allow_html=True)

# Состояние входа
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    # --- ЭКРАН РЕГИСТРАЦИИ ---
    st.markdown('<div class="main-title">cotakbass music</div>', unsafe_allow_html=True)
    
    # Контейнер для загрузки ФОНА
    st.markdown('<div class="glass-bg"></div>', unsafe_allow_html=True)
    st.file_uploader("bg", type=['png', 'jpg'], key="bg_hidden", label_visibility="collapsed")
    
    # Контейнер для загрузки АВАТАРКИ
    st.markdown('<div class="avatar-frame"></div>', unsafe_allow_html=True)
    st.file_uploader("ava", type=['png', 'jpg'], key="ava_hidden", label_visibility="collapsed")
    
    # Поля ввода
    _, col_mid, _ = st.columns([0.3, 0.4, 0.3])
    with col_mid:
        username = st.text_input("name", placeholder="name")
        bio = st.text_input("bio", placeholder="biography")
        
        # Кнопка ДВЕРЬ
        st.write("<div class='login-btn-container'>", unsafe_allow_html=True)
        if st.button("🚪"): # Иконка двери в стиле фиолетовой линии
            if username:
                st.session_state.auth = True
                st.session_state.user_name = username
                st.rerun()
        st.write("</div>", unsafe_allow_html=True)

else:
    # ГЛАВНЫЙ ЭКРАН (Плеер)
    st.markdown(f'<h1 style="text-align:center; margin-top:20vh;">welcome, {st.session_state.user_name}</h1>', unsafe_allow_html=True)
    if st.button("← logout"):
        st.session_state.auth = False
        st.rerun()
