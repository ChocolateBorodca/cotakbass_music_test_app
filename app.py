import streamlit as st
import os
import base64

st.set_page_config(page_title="cotakbass", layout="wide", initial_sidebar_state="collapsed")

# Функция для отображения фото
def get_image_64(file):
    if file: return base64.b64encode(file.getvalue()).decode()
    return None

# Твой стиль по рисунку
st.markdown(f"""
    <style>
    header, footer, #MainMenu, [data-testid="stInputInstructions"] {{ visibility: hidden !important; }}
    .stApp {{ background-color: #000000; color: #FFFFFF; font-family: -apple-system, sans-serif; }}

    /* Заголовок как на рисунке */
    .draw-title {{
        font-size: 40px; font-weight: 300; letter-spacing: 5px;
        text-align: center; margin-top: 20px; margin-bottom: 30px;
        color: #FFFFFF;
    }}

    /* Прямоугольник с плюсиком (Фон) */
    .draw-bg-box {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        height: 120px; width: 100%; max-width: 450px;
        margin: 0 auto;
        position: relative;
        display: flex; align-items: center; justify-content: center;
        font-size: 30px; color: rgba(160, 32, 240, 0.5);
    }}

    /* Круг с плюсиком (Ава) */
    .draw-ava-circle {{
        width: 110px; height: 110px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 2px solid #A020F0;
        border-radius: 50%;
        margin: 20px auto;
        position: relative;
        display: flex; align-items: center; justify-content: center;
        overflow: hidden;
        font-size: 30px; color: #A020F0;
    }}
    .preview-img {{ width: 100%; height: 100%; object-fit: cover; position: absolute; }}

    /* Стеклянные капсулы ввода */
    div[data-testid="stTextInput"] div[data-baseweb="input"] {{
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 30px !important;
        max-width: 300px; margin: 0 auto;
    }}
    div[data-testid="stTextInput"] input {{ text-align: center !important; color: white !important; padding: 10px !important; }}
    div[data-testid="stTextInput"] label {{ display: none !important; }}

    /* Маленькая дверь внизу */
    .door-container {{ display: flex; justify-content: center; margin-top: 30px; }}
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(160, 32, 240, 0.4) !important;
        border-radius: 50% !important;
        color: #A020F0 !important;
        width: 60px !important; height: 60px !important;
        font-size: 24px !important;
    }}

    /* Скрытый загрузчик поверх боксов */
    .stFileUploader {{ position: absolute; opacity: 0; z-index: 100; cursor: pointer; }}
    </style>
""", unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="draw-title">cotakbass</div>', unsafe_allow_html=True)
    
    # Прямоугольник (ФОН)
    _, bg_c, _ = st.columns([0.2, 0.6, 0.2])
    with bg_c:
        st.markdown('<div class="draw-bg-box">+</div>', unsafe_allow_html=True)
        st.file_uploader("bg", type=['png', 'jpg'], key="bg_up", label_visibility="collapsed")
    
    # Круг (АВАТАРКА)
    st.markdown('<div class="draw-ava-circle">', unsafe_allow_html=True)
    ava_file = st.file_uploader("ava", type=['png', 'jpg'], key="ava_up", label_visibility="collapsed")
    base64_ava = get_image_64(ava_file)
    if base64_ava:
        st.markdown(f'<img src="data:image/png;base64,{base64_ava}" class="preview-img">', unsafe_allow_html=True)
    else:
        st.write("+")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Инпуты
    st.text_input("name", placeholder="name", key="n")
    st.text_input("status", placeholder="status", key="s")
    
    # Дверь
    st.markdown('<div class="door-container">', unsafe_allow_html=True)
    if st.button("🚪"):
        if st.session_state.n:
            st.session_state.auth = True
            st.session_state.user = st.session_state.n
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # ПЛЕЕР (Твой основной код)
    st.markdown(f'<h2 style="text-align:center; margin-top:20vh;">welcome, {st.session_state.user}</h2>', unsafe_allow_html=True)
    if st.button("logout"):
        st.session_state.auth = False
        st.rerun()
