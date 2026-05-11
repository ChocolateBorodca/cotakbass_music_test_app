import streamlit as st
import os
import base64

# Конфигурация
st.set_page_config(page_title="cotakbass music", layout="wide", initial_sidebar_state="collapsed")

# Стили для создания "жидкого стекла" и Apple дизайна
st.markdown(f"""
    <style>
    header, footer, #MainMenu, [data-testid="stInputInstructions"] {{ visibility: hidden !important; }}
    .stApp {{ background-color: #000000; color: #FFFFFF; font-family: -apple-system, sans-serif; }}

    /* Название приложения (как на главном) */
    .main-title {{
        font-size: 48px; font-weight: 800; letter-spacing: -2px;
        text-align: center; color: #FFFFFF;
        text-shadow: 0 0 20px rgba(160, 32, 240, 0.6);
        margin-bottom: 40px;
    }}

    /* Стеклянный прямоугольник для фона */
    .glass-bg-upload {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        height: 150px;
        width: 100%;
        max-width: 500px;
        margin: 0 auto 20px auto;
        display: flex; align-items: center; justify-content: center;
    }}

    /* Круглая аватарка в центре */
    .avatar-upload-container {{
        width: 150px; height: 150px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 2px solid #A020F0;
        border-radius: 50%;
        margin: -75px auto 30px auto; /* Наползает на фон */
        display: flex; align-items: center; justify-content: center;
        overflow: hidden;
    }}

    /* Стеклянные поля ввода */
    div[data-testid="stTextInput"] div[data-baseweb="input"] {{
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
    }}
    div[data-testid="stTextInput"] label {{ display: none !important; }}

    /* Круглые стеклянные кнопки */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(30px) !important;
        border: 1px solid rgba(160, 32, 240, 0.3) !important;
        border-radius: 50% !important;
        color: white !important;
        width: 70px !important; height: 70px !important;
        transition: 0.3s ease;
    }}
    
    /* Кнопка войти в углу */
    .login-corner {{
        position: fixed;
        bottom: 40px;
        right: 40px;
    }}
    </style>
""", unsafe_allow_html=True)

# Состояние входа
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    # --- ЭКРАН РЕГИСТРАЦИИ ---
    st.markdown('<div class="main-title">cotakbass music</div>', unsafe_allow_html=True)
    
    # 1. Стеклянный фон профиля
    st.markdown('<div class="glass-bg-upload">', unsafe_allow_html=True)
    bg_file = st.file_uploader("фон", type=['png', 'jpg'], key="bg_up", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. Аватарка (круглая кнопка)
    st.markdown('<div class="avatar-upload-container">', unsafe_allow_html=True)
    ava_file = st.file_uploader("ава", type=['png', 'jpg'], key="ava_up", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 3. Поле для имени
    col1, col2, col3 = st.columns([0.3, 0.4, 0.3])
    with col2:
        username = st.text_input("", placeholder="твое имя...")
        bio = st.text_input("", placeholder="о себе (статус)...")

    # 4. Кнопка войти в углу
    st.markdown('<div class="login-corner">', unsafe_allow_html=True)
    if st.button("GO"):
        if username:
            st.session_state.auth = True
            st.session_state.user_name = username
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Здесь твой основной код плеера
    st.write(f"Добро пожаловать, {st.session_state.user_name}!")
    if st.button("Выйти"):
        st.session_state.auth = False
        st.rerun()
