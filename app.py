import streamlit as st
import os
import base64

# Настройки
st.set_page_config(page_title="cotakbass", layout="wide", initial_sidebar_state="collapsed")

def get_base64(file):
    return base64.b64encode(file.getvalue()).decode() if file else None

# Инициализация авы
if 'user_ava' not in st.session_state: st.session_state.user_ava = None
if 'page' not in st.session_state: st.session_state.page = "main"

# УЛЬТРА-ФИКС: Только центр, только хардкор
st.markdown(f"""
    <style>
    /* Прячем всё лишнее от Streamlit */
    header, footer, #MainMenu, [data-testid="stInputInstructions"], 
    .st-emotion-cache-oc994i, .st-emotion-cache-1vt4y65, .st-emotion-cache-k7vsyb,
    [data-testid="stHeader"] {{
        display: none !important;
    }}
    
    .stApp {{ background-color: #000000; }}

    /* КНОПКА НАЗАД (СЛЕВА ВВЕРХУ) */
    .back-btn {{
        position: fixed;
        top: 30px;
        left: 30px;
        z-index: 9999;
    }}
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(160, 32, 240, 0.5) !important;
        border-radius: 50% !important;
        color: #A020F0 !important;
        width: 55px !important; height: 55px !important;
    }}

    /* ГЛАВНЫЙ КРУГ - РОВНО В ЦЕНТРЕ ЭКРАНА */
    .center-circle {{
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%); /* Сдвиг на половину себя назад для идеального центра */
        width: 200px;
        height: 200px;
        border-radius: 50%;
        border: 2px solid #A020F0;
        background: rgba(160, 32, 240, 0.05);
        backdrop-filter: blur(20px);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 60px;
        color: #A020F0;
        overflow: hidden;
        box-shadow: 0 0 40px rgba(160, 32, 240, 0.3);
        z-index: 1000;
    }}
    .center-circle img {{ width: 100%; height: 100%; object-fit: cover; }}

    /* Невидимый загрузчик на весь экран, но кликабельный только в центре */
    [data-testid="stFileUploader"] {{
        position: fixed !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: 200px !important;
        height: 200px !important;
        opacity: 0 !important;
        z-index: 1001 !important;
        cursor: pointer !important;
    }}
    </style>
""", unsafe_allow_html=True)

if st.session_state.page == "profile":
    # Кнопка назад
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("←"):
        st.session_state.page = "main"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Круг в центре
    if st.session_state.user_ava:
        st.markdown(f'<div class="center-circle"><img src="data:image/png;base64,{st.session_state.user_ava}"></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="center-circle">+</div>', unsafe_allow_html=True)

    # Загрузчик (привязан к центру)
    up = st.file_uploader("", key="ava_up", label_visibility="collapsed")
    if up:
        st.session_state.user_ava = get_base64(up)
        st.rerun()
else:
    # ГЛАВНЫЙ ЭКРАН (Упрощенно, чтобы ты проверил профиль)
    st.markdown('<div style="text-align:center; margin-top:40vh;">', unsafe_allow_html=True)
    if st.button("👤 ПРОФИЛЬ"):
        st.session_state.page = "profile"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
