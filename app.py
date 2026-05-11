import streamlit as st
import os

st.set_page_config(page_title="cotakbass music", layout="wide", initial_sidebar_state="collapsed")

# CSS: Ультра-зачистка и матовое стекло
st.markdown(f"""
    <style>
    header, footer, #MainMenu, [data-testid="stInputInstructions"] {{ visibility: hidden !important; }}
    .stApp {{ background-color: #000000; color: #FFFFFF; font-family: -apple-system, sans-serif; }}

    /* УБИРАЕМ КНОПКИ UPLOAD */
    [data-testid="stFileUploader"] {{
        position: absolute;
        width: 100%;
        height: 100%;
        opacity: 0; /* Делаем их полностью невидимыми */
        z-index: 10;
        cursor: pointer;
    }}

    /* Прямоугольник ФОНА */
    .glass-bg-box {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        height: 180px; width: 100%; max-width: 550px;
        margin: 0 auto;
        position: relative;
    }}

    /* Круг АВАТАРКИ */
    .avatar-circle-box {{
        width: 140px; height: 140px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(30px);
        border: 2px solid #A020F0;
        border-radius: 50%;
        margin: -70px auto 40px auto;
        position: relative;
        z-index: 5;
    }}

    /* Поля ввода (Стеклянные) */
    div[data-testid="stTextInput"] div[data-baseweb="input"] {{
        background: rgba(255, 255, 255, 0.04) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 15px !important;
    }}
    div[data-testid="stTextInput"] input {{ text-align: center !important; color: white !important; }}
    div[data-testid="stTextInput"] label {{ display: none !important; }}

    /* Кнопка ДВЕРЬ ПО ЦЕНТРУ */
    .door-container {{
        display: flex;
        justify-content: center;
        margin-top: 40px;
        width: 100%;
    }}
    
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(40px) !important;
        border: 1px solid rgba(160, 32, 240, 0.4) !important;
        border-radius: 50% !important;
        color: #A020F0 !important;
        width: 80px !important; height: 80px !important;
        font-size: 32px !important;
        transition: 0.3s !important;
    }}
    div.stButton > button:hover {{ border-color: #A020F0 !important; transform: scale(1.1); }}
    </style>
""", unsafe_allow_html=True)

# Инициализация входа
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    # --- ЭКРАН РЕГИСТРАЦИИ ---
    st.markdown('<h1 style="text-align:center; font-weight:800; margin-bottom:50px;">cotakbass music</h1>', unsafe_allow_html=True)
    
    # Слой ФОНА
    st.markdown('<div class="glass-bg-box">', unsafe_allow_html=True)
    st.file_uploader("bg", type=['png', 'jpg'], key="bg_up", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Слой АВАТАРКИ
    st.markdown('<div class="avatar-circle-box">', unsafe_allow_html=True)
    st.file_uploader("ava", type=['png', 'jpg'], key="ava_up", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Поля name и biography
    _, col_mid, _ = st.columns([0.3, 0.4, 0.3])
    with col_mid:
        u_name = st.text_input("name", placeholder="name")
        u_bio = st.text_input("biography", placeholder="biography")
        
        # Кнопка ДВЕРЬ в центре
        st.markdown('<div class="door-container">', unsafe_allow_html=True)
        if st.button("🚪"):
            if u_name:
                st.session_state.auth = True
                st.session_state.user = u_name
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- ГЛАВНЫЙ ЭКРАН ПЛЕЕРА ---
    # (Здесь должен быть твой старый код плеера со всеми кнопками ❮ ▶ ❯ ♥)
    st.markdown('<div style="text-align:center; margin-top:10vh;">', unsafe_allow_html=True)
    st.write(f"player active: {st.session_state.user}")
    # Чтобы вернуться назад для теста, можешь добавить мелкую кнопку в углу
    if st.button("exit", key="exit_btn"):
        st.session_state.auth = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
