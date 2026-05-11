import streamlit as st
import os
import base64

st.set_page_config(page_title="cotakbass music", layout="wide", initial_sidebar_state="collapsed")

# Функция для превью
def get_image_base64(file):
    if file is not None:
        return base64.b64encode(file.getvalue()).decode()
    return None

# УЛЬТРА-ФИКС ДИЗАЙНА
st.markdown(f"""
    <style>
    /* 1. Полная зачистка мусора */
    header, footer, #MainMenu, [data-testid="stInputInstructions"], 
    .st-emotion-cache-oc994i, .st-emotion-cache-1pxm666 {{
        display: none !important;
        height: 0 !important;
    }}

    .stApp {{ background-color: #000000; color: #FFFFFF; font-family: -apple-system, sans-serif; }}

    /* 2. Скрытые загрузчики поверх фигур */
    [data-testid="stFileUploader"] {{
        position: absolute;
        width: 100%;
        height: 100%;
        opacity: 0;
        z-index: 100;
        cursor: pointer;
    }}
    [data-testid="stFileUploader"] section {{ display: none !important; }}

    /* 3. Прямоугольник ФОНА */
    .bg-container {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        height: 180px; width: 100%; max-width: 550px;
        margin: 0 auto;
        position: relative;
        display: flex; align-items: center; justify-content: center;
    }}

    /* 4. Круг АВАТАРКИ */
    .ava-container {{
        width: 140px; height: 140px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(30px);
        border: 2px solid #A020F0;
        border-radius: 50%;
        margin: -70px auto 40px auto;
        position: relative;
        z-index: 50;
        overflow: hidden;
        display: flex; align-items: center; justify-content: center;
    }}
    .preview-img {{ width: 100%; height: 100%; object-fit: cover; position: absolute; }}

    /* 5. Поля ввода (Капсулы) */
    div[data-testid="stTextInput"] div[data-baseweb="input"] {{
        background: rgba(255, 255, 255, 0.04) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px !important;
        max-width: 400px; margin: 0 auto;
    }}
    div[data-testid="stTextInput"] input {{ text-align: center !important; color: white !important; }}
    div[data-testid="stTextInput"] label {{ display: none !important; }}

    /* 6. Кнопка ДВЕРЬ (ЦЕНТР) */
    .door-box {{
        display: flex;
        justify-content: center;
        margin-top: 40px;
        width: 100%;
    }}
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(160, 32, 240, 0.4) !important;
        border-radius: 50% !important;
        color: #A020F0 !important;
        width: 70px !important; height: 70px !important;
        font-size: 32px !important;
        transition: 0.3s !important;
    }}
    </style>
""", unsafe_allow_html=True)

# Логика входа
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<h1 style="text-align:center; font-weight:800; margin-bottom:50px;">cotakbass music</h1>', unsafe_allow_html=True)
    
    # ЗОНА ФОНА
    st.markdown('<div class="bg-container">', unsafe_allow_html=True)
    st.file_uploader("bg", type=['png', 'jpg'], key="bg_up", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ЗОНА АВЫ
    st.markdown('<div class="ava-container">', unsafe_allow_html=True)
    ava_file = st.file_uploader("ava", type=['png', 'jpg'], key="ava_up", label_visibility="collapsed")
    img_data = get_image_base64(ava_file)
    if img_data:
        st.markdown(f'<img src="data:image/png;base64,{img_data}" class="preview-img">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ИНПУТЫ
    _, col_mid, _ = st.columns([0.2, 0.6, 0.2])
    with col_mid:
        u_name = st.text_input("name", placeholder="name")
        u_bio = st.text_input("biography", placeholder="biography")
        
        # ДВЕРЬ
        st.markdown('<div class="door-box">', unsafe_allow_html=True)
        if st.button("🚪"):
            if u_name:
                st.session_state.auth = True
                st.session_state.user = u_name
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Здесь открывается твой основной плеер
    st.markdown(f'<h2 style="text-align:center; margin-top:20vh;">welcome, {st.session_state.user}</h2>', unsafe_allow_html=True)
    if st.button("logout"):
        st.session_state.auth = False
        st.rerun()
