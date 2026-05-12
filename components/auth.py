import streamlit as st
import base64

def get_base64_img(file):
    if file: return base64.b64encode(file.getvalue()).decode()
    return None

def registration_screen():
    st.markdown("""
        <style>
        /* 1. ПОЛНАЯ ЗАЧИСТКА: Убираем белые точки и системные элементы */
        header, footer, #MainMenu, [data-testid="stInputInstructions"], 
        .st-emotion-cache-oc994i, .st-emotion-cache-1pxm666, .st-emotion-cache-1vt4y65 {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
        }

        .stApp { background-color: #000000; color: white; font-family: -apple-system, sans-serif; }

        /* 2. ЦЕНТРАЛЬНАЯ АВАТАРКА: Рабочая зона */
        .upload-container {
            position: relative;
            width: 140px; height: 140px;
            margin: 40px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 50;
        }
        
        /* Растягиваем невидимый загрузчик точно на круг */
        [data-testid="stFileUploader"] {
            position: absolute !important;
            inset: 0 !important;
            width: 100% !important;
            height: 100% !important;
            opacity: 0 !important;
            z-index: 1000 !important;
            cursor: pointer !important;
        }

        .ava-visual { 
            width: 100%; height: 100%;
            background: rgba(255, 255, 255, 0.05); 
            backdrop-filter: blur(30px); 
            border: 2px solid #A020F0; 
            border-radius: 50%; 
            display: flex; align-items: center; justify-content: center; 
            font-size: 40px; color: #A020F0; 
            overflow: hidden;
            box-shadow: 0 0 20px rgba(160, 32, 240, 0.2);
        }
        .preview-img { width: 100%; height: 100%; object-fit: cover; position: absolute; }

        /* 3. ИНПУТЫ */
        div[data-testid="stTextInput"] div[data-baseweb="input"] { 
            background: rgba(255, 255, 255, 0.04) !important; 
            border: 1px solid rgba(255, 255, 255, 0.1) !important; 
            border-radius: 25px !important; 
            max-width: 300px; margin: 0 auto; 
        }
        div[data-testid="stTextInput"] input { text-align: center !important; color: white !important; }
        div[data-testid="stTextInput"] label { display: none !important; }

        /* 4. КНОПКА ДВЕРЬ - СТРОГО ПО ЦЕНТРУ */
        .door-wrapper {
            display: flex;
            justify-content: center;
            width: 100%;
            margin-top: 40px;
        }
        .door-wrapper button { 
            background: rgba(255, 255, 255, 0.02) !important; 
            border: 1px solid rgba(160, 32, 240, 0.5) !important; 
            border-radius: 50% !important; 
            color: #A020F0 !important; 
            width: 75px !important; height: 75px !important; 
            font-size: 30px !important; 
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 style="text-align:center; font-weight:200; margin-top:30px;">cotakbass</h1>', unsafe_allow_html=True)
    
    # КРУГ В ЦЕНТРЕ
    st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    st.markdown('<div class="ava-visual">', unsafe_allow_html=True)
    u_ava = st.file_uploader("", key="reg_ava")
    img_64 = get_base64_img(u_ava)
    if img_64: 
        st.markdown(f'<img src="data:image/png;base64,{img_64}" class="preview-img">', unsafe_allow_html=True)
        st.session_state.user['ava'] = img_64
    else: 
        st.write("+")
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # ПОЛЯ
    st.text_input("name", placeholder="name", key="reg_n")
    st.write("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.text_input("status", placeholder="status", key="reg_s")
    
    # ДВЕРЬ
    st.markdown('<div class="door-wrapper">', unsafe_allow_html=True)
    if st.button("🚪"):
        if st.session_state.reg_n:
            st.session_state.auth = True
            st.session_state.user['name'] = st.session_state.reg_n
            st.session_state.page = "main"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
