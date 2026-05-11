import streamlit as st
import os
import base64

st.set_page_config(page_title="cotakbass music", layout="wide", initial_sidebar_state="collapsed")

# Вспомогательная функция для отображения загруженных фото
def get_image_base64(file):
    if file is not None:
        return base64.b64encode(file.getvalue()).decode()
    return None

# Ультра-CSS фикс
st.markdown(f"""
    <style>
    header, footer, #MainMenu, [data-testid="stInputInstructions"] {{ visibility: hidden !important; }}
    .stApp {{ background-color: #000000; color: #FFFFFF; font-family: -apple-system, sans-serif; }}

    /* Прячем стандартные загрузчики, но оставляем их активными под кнопками */
    .hidden-uploader {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; z-index: 10; cursor: pointer; }}

    /* Прямоугольник ФОНА */
    .glass-bg-box {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        height: 180px; width: 100%; max-width: 550px;
        margin: 0 auto;
        position: relative;
        overflow: hidden;
        display: flex; align-items: center; justify-content: center;
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
        z-index: 20;
        overflow: hidden;
        display: flex; align-items: center; justify-content: center;
    }}
    .avatar-img {{ width: 100%; height: 100%; object-fit: cover; }}

    /* Поля ввода (БЕЗ перекрытия слоями) */
    div[data-testid="stTextInput"] {{ position: relative; z-index: 30 !important; }}
    div[data-testid="stTextInput"] div[data-baseweb="input"] {{
        background: rgba(255, 255, 255, 0.04) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 15px !important;
    }}
    div[data-testid="stTextInput"] input {{ text-align: center !important; color: white !important; font-size: 16px !important; }}
    div[data-testid="stTextInput"] label {{ display: none !important; }}

    /* Кнопка ДВЕРЬ ПО ЦЕНТРУ */
    .door-container {{ display: flex; justify-content: center; margin-top: 40px; width: 100%; position: relative; z-index: 40; }}
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(40px) !important;
        border: 1px solid rgba(160, 32, 240, 0.4) !important;
        border-radius: 50% !important;
        color: #A020F0 !important;
        width: 80px !important; height: 80px !important;
        font-size: 32px !important;
    }}
    </style>
""", unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<h1 style="text-align:center; font-weight:800; margin-bottom:50px;">cotakbass music</h1>', unsafe_allow_html=True)
    
    # 1. ЗОНА ФОНА
    bg_col1, bg_col_mid, bg_col3 = st.columns([0.2, 0.6, 0.2])
    with bg_col_mid:
        st.markdown('<div class="glass-bg-box">', unsafe_allow_html=True)
        # Если фон загружен, показываем его (здесь можно добавить превью фона аналогично аве)
        st.file_uploader("bg", type=['png', 'jpg'], key="bg_up", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. ЗОНА АВАТАРКИ (с предпросмотром)
    st.markdown('<div class="avatar-circle-box">', unsafe_allow_html=True)
    ava_file = st.file_uploader("ava", type=['png', 'jpg'], key="ava_up", label_visibility="collapsed")
    base64_ava = get_image_base64(ava_file)
    if base64_ava:
        st.markdown(f'<img src="data:image/png;base64,{base64_ava}" class="avatar-img">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 3. ПОЛЯ ВВОДА (Центрированные)
    _, col_mid, _ = st.columns([0.3, 0.4, 0.3])
    with col_mid:
        u_name = st.text_input("name", placeholder="name", key="input_name")
        u_bio = st.text_input("biography", placeholder="biography", key="input_bio")
        
        # 4. КНОПКА ДВЕРЬ
        st.markdown('<div class="door-container">', unsafe_allow_html=True)
        if st.button("🚪"):
            if u_name:
                st.session_state.auth = True
                st.session_state.user = u_name
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # ГЛАВНЫЙ ЭКРАН ПЛЕЕРА
    st.markdown(f'<h2 style="text-align:center; margin-top:20vh;">welcome, {st.session_state.user}</h2>', unsafe_allow_html=True)
    if st.button("logout"):
        st.session_state.auth = False
        st.rerun()
