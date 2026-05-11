import streamlit as st
import os
import base64

st.set_page_config(page_title="cotakbass", layout="wide", initial_sidebar_state="collapsed")

# Функция для конвертации картинки в base64
def img_to_64(file):
    if file: return base64.b64encode(file.getvalue()).decode()
    return None

# Ультра-CSS фикс
st.markdown(f"""
    <style>
    header, footer, #MainMenu, [data-testid="stInputInstructions"] {{ visibility: hidden !important; }}
    .stApp {{ background-color: #000000; color: #FFFFFF; font-family: -apple-system, sans-serif; }}

    /* Убираем белые точки и системные элементы загрузки */
    [data-testid="stFileUploader"] {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; z-index: 100; cursor: pointer; }}
    [data-testid="stFileUploader"] section {{ display: none !important; }}
    .st-emotion-cache-oc994i {{ display: none !important; }} /* Скрывает индикатор загрузки (белую точку) */

    /* Заголовок */
    .draw-title {{ font-size: 44px; font-weight: 200; letter-spacing: 6px; text-align: center; margin: 30px 0; }}

    /* Стеклянный ФОН (Кликабельный) */
    .bg-area {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 22px;
        height: 140px; width: 100%; max-width: 500px;
        margin: 0 auto;
        position: relative;
        display: flex; align-items: center; justify-content: center;
        font-size: 36px; color: rgba(160, 32, 240, 0.6);
    }}

    /* Стеклянная АВАТАРКА (Кликабельная) */
    .ava-area {{
        width: 120px; height: 120px;
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(20px);
        border: 2px solid #A020F0;
        border-radius: 50%;
        margin: 20px auto;
        position: relative;
        display: flex; align-items: center; justify-content: center;
        overflow: hidden;
        font-size: 34px; color: #A020F0;
    }}
    .ava-img {{ width: 100%; height: 100%; object-fit: cover; position: absolute; z-index: 5; }}

    /* Поля ввода-капсулы */
    div[data-testid="stTextInput"] div[data-baseweb="input"] {{
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 30px !important;
        max-width: 320px; margin: 0 auto;
    }}
    div[data-testid="stTextInput"] input {{ text-align: center !important; color: white !important; padding: 12px !important; }}
    div[data-testid="stTextInput"] label {{ display: none !important; }}

    /* Кнопка ДВЕРЬ (Центрированная) */
    .door-box {{ display: flex; justify-content: center; margin-top: 35px; width: 100%; }}
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(160, 32, 240, 0.4) !important;
        border-radius: 50% !important;
        color: #A020F0 !important;
        width: 65px !important; height: 65px !important;
        font-size: 26px !important;
        transition: 0.3s ease;
    }}
    div.stButton > button:hover {{ border-color: #A020F0 !important; transform: scale(1.05); }}
    </style>
""", unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="draw-title">cotakbass</div>', unsafe_allow_html=True)
    
    # Секция ФОНА
    _, col_bg, _ = st.columns([0.2, 0.6, 0.2])
    with col_bg:
        st.markdown('<div class="bg-area">+</div>', unsafe_allow_html=True)
        st.file_uploader("bg", type=['png', 'jpg'], key="bg_up", label_visibility="collapsed")
    
    # Секция АВАТАРКИ
    st.markdown('<div class="ava-area">', unsafe_allow_html=True)
    ava_file = st.file_uploader("ava", type=['png', 'jpg'], key="ava_up", label_visibility="collapsed")
    base64_img = img_to_64(ava_file)
    if base64_img:
        st.markdown(f'<img src="data:image/png;base64,{base64_img}" class="ava-img">', unsafe_allow_html=True)
    else:
        st.write("+")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Инпуты (Никаких точек рядом!)
    st.text_input("name", placeholder="name", key="name_input")
    st.text_input("status", placeholder="status", key="status_input")
    
    # Кнопка ДВЕРЬ (Центр)
    st.markdown('<div class="door-box">', unsafe_allow_html=True)
    if st.button("🚪"):
        if st.session_state.name_input:
            st.session_state.auth = True
            st.session_state.user = st.session_state.name_input
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Твой основной плеер
    st.markdown(f'<h2 style="text-align:center; margin-top:20vh;">welcome, {st.session_state.user}</h2>', unsafe_allow_html=True)
    if st.button("exit"):
        st.session_state.auth = False
        st.rerun()
