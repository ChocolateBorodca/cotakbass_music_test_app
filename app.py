import streamlit as st
import os
import base64

st.set_page_config(page_title="cotakbass", layout="wide", initial_sidebar_state="collapsed")

def img_to_64(file):
    if file: return base64.b64encode(file.getvalue()).decode()
    return None

# МАКСИМАЛЬНЫЙ CSS ФИКС
st.markdown(f"""
    <style>
    /* 1. Полная зачистка мусора Streamlit */
    header, footer, #MainMenu, [data-testid="stInputInstructions"], .st-emotion-cache-1pxm666 {{
        display: none !important;
    }}
    
    /* Убираем белые точки и системные кнопки загрузки везде */
    [data-testid="stFileUploader"] section {{ display: none !important; }}
    [data-testid="stFileUploader"] {{ 
        position: absolute; 
        top: 0; left: 0; width: 100%; height: 100%; 
        opacity: 0; z-index: 1000; cursor: pointer; 
    }}

    .stApp {{ background-color: #000000; color: #FFFFFF; font-family: -apple-system, sans-serif; }}

    /* Заголовок */
    .draw-title {{ font-size: 40px; font-weight: 200; letter-spacing: 5px; text-align: center; margin: 30px 0; }}

    /* КОНТЕЙНЕР ДЛЯ ФОНА (Прямоугольник) */
    .bg-wrapper {{
        position: relative;
        width: 100%; max-width: 450px;
        height: 130px;
        margin: 0 auto;
    }}
    .bg-area {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        width: 100%; height: 100%;
        display: flex; align-items: center; justify-content: center;
        font-size: 30px; color: rgba(160, 32, 240, 0.5);
    }}

    /* КОНТЕЙНЕР ДЛЯ АВЫ (Круг) */
    .ava-wrapper {{
        position: relative;
        width: 110px; height: 110px;
        margin: 20px auto;
    }}
    .ava-area {{
        width: 100%; height: 100%;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 2px solid #A020F0;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        overflow: hidden;
        font-size: 30px; color: #A020F0;
    }}
    .ava-img {{ width: 100%; height: 100%; object-fit: cover; position: absolute; top:0; left:0; }}

    /* Инпуты-капсулы */
    .input-container {{ width: 100%; max-width: 320px; margin: 0 auto; }}
    div[data-testid="stTextInput"] div[data-baseweb="input"] {{
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 30px !important;
    }}
    div[data-testid="stTextInput"] input {{ text-align: center !important; color: white !important; }}
    div[data-testid="stTextInput"] label {{ display: none !important; }}

    /* Кнопка ДВЕРЬ - СТРОГО ПО ЦЕНТРУ */
    .door-wrapper {{
        display: flex;
        justify-content: center;
        width: 100%;
        margin-top: 30px;
    }}
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(160, 32, 240, 0.5) !important;
        border-radius: 50% !important;
        color: #A020F0 !important;
        width: 65px !important; height: 65px !important;
        font-size: 26px !important;
    }}
    </style>
""", unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="draw-title">cotakbass</div>', unsafe_allow_html=True)
    
    # Прямоугольник (ФОН)
    st.markdown('<div class="bg-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="bg-area">+</div>', unsafe_allow_html=True)
    st.file_uploader("", type=['png', 'jpg'], key="bg_up")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Круг (АВАТАРКА)
    st.markdown('<div class="ava-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="ava-area">', unsafe_allow_html=True)
    ava_file = st.file_uploader("", type=['png', 'jpg'], key="ava_up")
    base64_img = img_to_64(ava_file)
    if base64_img:
        st.markdown(f'<img src="data:image/png;base64,{base64_img}" class="ava-img">', unsafe_allow_html=True)
    else:
        st.write("+")
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Поля ввода
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.text_input("name", placeholder="name", key="n_in")
    st.text_input("status", placeholder="status", key="s_in")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Дверь (Центр)
    st.markdown('<div class="door-wrapper">', unsafe_allow_html=True)
    if st.button("🚪"):
        if st.session_state.n_in:
            st.session_state.auth = True
            st.session_state.user = st.session_state.n_in
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Здесь твой главный экран плеера
    st.markdown(f'<h2 style="text-align:center; margin-top:20vh;">welcome, {st.session_state.user}</h2>', unsafe_allow_html=True)
    if st.button("logout"):
        st.session_state.auth = False
        st.rerun()
