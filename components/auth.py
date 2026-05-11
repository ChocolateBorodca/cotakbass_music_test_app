import streamlit as st
import base64

def get_base64_img(file):
    if file: return base64.b64encode(file.getvalue()).decode()
    return None

def registration_screen():
    st.markdown("""
        <style>
        /* 1. ПОЛНАЯ ЗАЧИСТКА СИСТЕМНОГО МУСОРА */
        header, footer, #MainMenu, [data-testid="stInputInstructions"], 
        .st-emotion-cache-oc994i, .st-emotion-cache-1pxm666, .st-emotion-cache-1vt4y65 {
            display: none !important;
            visibility: hidden !important;
        }

        .stApp { background-color: #000000; color: white; font-family: -apple-system, sans-serif; }

        /* 2. ЗОНЫ КЛИКА (Прозрачный слой поверх фигур) */
        .upload-zone {
            position: relative;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* Растягиваем загрузчик */
        [data-testid="stFileUploader"] {
            position: absolute !important;
            inset: 0 !important;
            width: 100% !important;
            height: 100% !important;
            opacity: 0 !important;
            z-index: 1000 !important;
            cursor: pointer !important;
        }
        [data-testid="stFileUploader"] section { padding: 0 !important; height: 100% !important; }

        /* 3. ВИЗУАЛ ПРЯМОУГОЛЬНИКА */
        .bg-box-visual { 
            background: rgba(255,255,255,0.03); 
            backdrop-filter: blur(40px); 
            border: 1px solid rgba(255,255,255,0.1); 
            border-radius: 25px; 
            height: 150px; width: 100%; max-width: 480px; 
            display: flex; align-items: center; justify-content: center; 
            font-size: 32px; color: rgba(160, 32, 240, 0.4); 
        }

        /* 4. ВИЗУАЛ КРУГА */
        .ava-circle-visual { 
            width: 120px; height: 120px; 
            background: rgba(255, 255, 255, 0.05); 
            backdrop-filter: blur(30px); 
            border: 2px solid #A020F0; 
            border-radius: 50%; 
            margin-top: -60px;
            display: flex; align-items: center; justify-content: center; 
            font-size: 32px; color: #A020F0; 
            position: relative; z-index: 10;
            overflow: hidden;
        }
        .preview-img { width: 100%; height: 100%; object-fit: cover; position: absolute; inset: 0; }

        /* 5. ПОЛЯ ВВОДА */
        div[data-testid="stTextInput"] div[data-baseweb="input"] { 
            background: rgba(255, 255, 255, 0.04) !important; 
            border-radius: 25px !important; 
            max-width: 350px; margin: 0 auto; 
            border: 1px solid rgba(255,255,255,0.1) !important; 
        }
        div[data-testid="stTextInput"] input { text-align: center !important; color: white !important; }
        div[data-testid="stTextInput"] label { display: none !important; }

        /* 6. КНОПКА СТРЕЛКА (ЦЕНТР) */
        .center-btn-box { display: flex; justify-content: center; width: 100%; margin-top: 40px; }
        .center-btn-box button { 
            background: rgba(255, 255, 255, 0.02) !important; 
            border: 1px solid rgba(160, 32, 240, 0.5) !important; 
            border-radius: 50% !important; 
            color: #A020F0 !important; 
            width: 70px !important; height: 70px !important; 
            font-size: 30px !important;
            transition: 0.3s ease !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 style="text-align:center; font-weight:800; margin-bottom:40px; margin-top:20px;">cotakbass music</h1>', unsafe_allow_html=True)
    
    # ПРЯМОУГОЛЬНИК (ФОН)
    st.markdown('<div class="upload-zone" style="max-width:480px; height:150px;">', unsafe_allow_html=True)
    st.markdown('<div class="bg-box-visual">+</div>', unsafe_allow_html=True)
    st.file_uploader("bg", key="reg_bg")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # КРУГ (АВА)
    st.markdown('<div class="upload-zone" style="width:120px; height:120px; margin-top:-60px;">', unsafe_allow_html=True)
    st.markdown('<div class="ava-circle-visual">', unsafe_allow_html=True)
    u_ava = st.file_uploader("ava", key="reg_ava")
    img_64 = get_base64_img(u_ava)
    if img_64: st.markdown(f'<img src="data:image/png;base64,{img_64}" class="preview-img">', unsafe_allow_html=True)
    else: st.write("+")
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # ТЕКСТОВЫЕ ПОЛЯ
    st.write("<div style='height:40px'></div>", unsafe_allow_html=True)
    name = st.text_input("name", placeholder="name", key="reg_name")
    status = st.text_input("status", placeholder="status", key="reg_status")
    
    # КНОПКА СТРЕЛКА (ЦЕНТР)
    st.markdown('<div class="center-btn-box">', unsafe_allow_html=True)
    if st.button("❯"):
        if name:
            st.session_state.auth = True
            st.session_state.user_name = name
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
