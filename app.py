import streamlit as st
import os
import base64

st.set_page_config(page_title="cotakbass music", layout="wide", initial_sidebar_state="collapsed")

# Функция для конвертации картинки в превью
def get_image_base64(file):
    if file is not None:
        return base64.b64encode(file.getvalue()).decode()
    return None

# УЛЬТРА-CSS: Делаем фигуры реально кликабельными
st.markdown(f"""
    <style>
    /* 1. Зачистка системного мусора */
    header, footer, #MainMenu, [data-testid="stInputInstructions"], 
    .st-emotion-cache-oc994i, .st-emotion-cache-1pxm666, .st-emotion-cache-1vt4y65 {{
        display: none !important;
        height: 0 !important;
    }}

    .stApp {{ background-color: #000000; color: #FFFFFF; font-family: -apple-system, sans-serif; }}

    /* 2. ГЛАВНЫЙ СЕКРЕТ: Делаем невидимый загрузчик на всю площадь родителя */
    .upload-wrapper {{
        position: relative;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    
    /* Растягиваем стандартный загрузчик поверх нашей красоты */
    [data-testid="stFileUploader"] {{
        position: absolute !important;
        inset: 0 !important;
        width: 100% !important;
        height: 100% !important;
        opacity: 0 !important;
        z-index: 100 !important;
        cursor: pointer !important;
    }}
    [data-testid="stFileUploader"] section {{ padding: 0 !important; }}

    /* 3. Визуал ПРЯМОУГОЛЬНИКА */
    .bg-visual-box {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        height: 180px; width: 100%; max-width: 550px;
        display: flex; align-items: center; justify-content: center;
        font-size: 30px; color: rgba(160, 32, 240, 0.4);
    }}

    /* 4. Визуал КРУГА */
    .ava-visual-circle {{
        width: 140px; height: 140px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(30px);
        border: 2px solid #A020F0;
        border-radius: 50%;
        margin-top: -70px; /* Нахлест */
        overflow: hidden;
        display: flex; align-items: center; justify-content: center;
        font-size: 30px; color: #A020F0;
        position: relative;
        z-index: 10;
    }}
    .preview-img {{ width: 100%; height: 100%; object-fit: cover; position: absolute; inset: 0; }}

    /* 5. Поля ввода */
    div[data-testid="stTextInput"] div[data-baseweb="input"] {{
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px !important;
        max-width: 400px; margin: 0 auto;
    }}
    div[data-testid="stTextInput"] input {{ text-align: center !important; color: white !important; padding: 15px !important; }}
    div[data-testid="stTextInput"] label {{ display: none !important; }}

    /* 6. Кнопка СТРЕЛКА (ЦЕНТР) */
    .arrow-box {{
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
        font-size: 24px !important;
        transition: 0.3s !important;
    }}
    </style>
""", unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<h1 style="text-align:center; font-weight:800; margin-bottom:50px;">cotakbass music</h1>', unsafe_allow_html=True)
    
    # ЗОНА ФОНА (Кликабельный прямоугольник)
    st.markdown('<div class="upload-wrapper" style="max-width:550px; height:180px;">', unsafe_allow_html=True)
    st.markdown('<div class="bg-visual-box">+</div>', unsafe_allow_html=True)
    st.file_uploader("bg", type=['png', 'jpg'], key="bg_up")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ЗОНА АВАТАРКИ (Кликабельный круг)
    st.markdown('<div class="upload-wrapper" style="width:140px; height:140px; margin-top:-70px;">', unsafe_allow_html=True)
    st.markdown('<div class="ava-visual-circle">', unsafe_allow_html=True)
    ava_file = st.file_uploader("ava", type=['png', 'jpg'], key="ava_up")
    img_data = get_image_base64(ava_file)
    if img_data:
        st.markdown(f'<img src="data:image/png;base64,{img_data}" class="preview-img">', unsafe_allow_html=True)
    else:
        st.write("+")
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # ПОЛЯ ВВОДА
    st.write("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
    _, col_mid, _ = st.columns([0.2, 0.6, 0.2])
    with col_mid:
        u_name = st.text_input("name", placeholder="name", key="n")
        u_bio = st.text_input("biography", placeholder="biography", key="b")
        
        # СТРЕЛКА ВМЕСТО ДВЕРИ
        st.markdown('<div class="arrow-box">', unsafe_allow_html=True)
        if st.button("❯"):
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
