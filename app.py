import streamlit as st
import os
import base64

st.set_page_config(page_title="cotakbass", layout="wide", initial_sidebar_state="collapsed")

def img_to_64(file):
    if file: return base64.b64encode(file.getvalue()).decode()
    return None

# УЛЬТРА-ФИКС: Жёсткие размеры и удаление мусора
st.markdown(f"""
    <style>
    /* 1. ПОЛНАЯ ЗАЧИСТКА ВСЕГО СИСТЕМНОГО */
    header, footer, #MainMenu, [data-testid="stInputInstructions"], 
    .st-emotion-cache-1pxm666, .st-emotion-cache-oc994i, 
    [data-testid="stFileUploader"] section, .st-emotion-cache-1vt4y65 {{
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }}
    
    /* Делаем невидимый слой загрузки по всему экрану для фигур */
    [data-testid="stFileUploader"] {{ 
        position: absolute !important; 
        top: 0 !important; left: 0 !important; 
        width: 100% !important; height: 100% !important; 
        opacity: 0 !important; z-index: 1000 !important; 
        cursor: pointer !important; 
    }}

    .stApp {{ background-color: #000000; color: #FFFFFF; font-family: -apple-system, sans-serif; }}

    /* Заголовок */
    .draw-title {{ font-size: 38px; font-weight: 200; letter-spacing: 5px; text-align: center; margin: 20px 0; }}

    /* ПРЯМОУГОЛЬНИК ФОНА (Фиксированный размер) */
    .bg-wrapper {{
        position: relative;
        width: 90%; max-width: 450px;
        height: 150px; /* Фиксированная высота */
        margin: 0 auto;
    }}
    .bg-visual {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        width: 100%; height: 100%;
        display: flex; align-items: center; justify-content: center;
        font-size: 32px; color: rgba(160, 32, 240, 0.5);
    }}

    /* КРУГ АВАТАРКИ (Строго под фоном) */
    .ava-wrapper {{
        position: relative;
        width: 120px; height: 120px;
        margin: -60px auto 30px auto; /* Нахлёст на фон */
        z-index: 5;
    }}
    .ava-visual {{
        width: 100%; height: 100%;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(30px);
        border: 2px solid #A020F0;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        overflow: hidden;
        font-size: 32px; color: #A020F0;
    }}
    .ava-img {{ width: 100%; height: 100%; object-fit: cover; position: absolute; }}

    /* Инпуты-капсулы */
    .inputs-container {{ width: 90%; max-width: 320px; margin: 0 auto; }}
    div[data-testid="stTextInput"] div[data-baseweb="input"] {{
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 30px !important;
        margin-bottom: 10px;
    }}
    div[data-testid="stTextInput"] input {{ text-align: center !important; color: white !important; }}
    div[data-testid="stTextInput"] label {{ display: none !important; }}

    /* Кнопка ДВЕРЬ - ЦЕНТР */
    .door-box {{
        display: flex;
        justify-content: center;
        margin-top: 30px;
    }}
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(160, 32, 240, 0.5) !important;
        border-radius: 50% !important;
        color: #A020F0 !important;
        width: 75px !important; height: 75px !important;
        font-size: 30px !important;
    }}
    </style>
""", unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="draw-title">cotakbass</div>', unsafe_allow_html=True)
    
    # ФОН
    st.markdown('<div class="bg-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="bg-visual">+</div>', unsafe_allow_html=True)
    st.file_uploader("", type=['png', 'jpg'], key="bg_hidden")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # АВАТАРКА
    st.markdown('<div class="ava-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="ava-visual">', unsafe_allow_html=True)
    ava_file = st.file_uploader("", type=['png', 'jpg'], key="ava_hidden")
    base64_ava = img_to_64(ava_file)
    if base64_ava:
        st.markdown(f'<img src="data:image/png;base64,{base64_ava}" class="ava-img">', unsafe_allow_html=True)
    else:
        st.write("+")
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # ИНПУТЫ
    st.markdown('<div class="inputs-container">', unsafe_allow_html=True)
    name = st.text_input("name", placeholder="name", key="n_val")
    status = st.text_input("status", placeholder="status", key="s_val")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ДВЕРЬ
    st.markdown('<div class="door-box">', unsafe_allow_html=True)
    if st.button("🚪"):
        if st.session_state.n_val:
            st.session_state.auth = True
            st.session_state.user = st.session_state.n_val
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Здесь твой старый код плеера
    st.markdown(f'<h2 style="text-align:center; margin-top:20vh;">welcome, {st.session_state.user}</h2>', unsafe_allow_html=True)
    if st.button("logout"):
        st.session_state.auth = False
        st.rerun()
