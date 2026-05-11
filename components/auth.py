import streamlit as st
import base64

def get_base64_img(file):
    return base64.b64encode(file.getvalue()).decode() if file else None

def registration_screen():
    st.markdown("""
        <style>
        header, footer, #MainMenu, [data-testid="stInputInstructions"], .st-emotion-cache-oc994i { display: none !important; }
        .stApp { background-color: #000000; color: white; }
        
        /* ЗОНЫ КЛИКА */
        .upload-wrapper { position: relative; margin: 0 auto; display: flex; align-items: center; justify-content: center; }
        [data-testid="stFileUploader"] {
            position: absolute !important; inset: 0 !important;
            width: 100% !important; height: 100% !important;
            opacity: 0 !important; z-index: 1000 !important; cursor: pointer !important;
            pointer-events: auto !important;
        }

        .bg-draw { background: rgba(255,255,255,0.03); backdrop-filter: blur(40px); border: 1px solid rgba(255,255,255,0.1); border-radius: 30px; height: 160px; width: 100%; max-width: 500px; display: flex; align-items: center; justify-content: center; font-size: 32px; color: rgba(160, 32, 240, 0.4); }
        .ava-draw { width: 130px; height: 130px; background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(30px); border: 2px solid #A020F0; border-radius: 50%; margin-top: -65px; overflow: hidden; display: flex; align-items: center; justify-content: center; font-size: 32px; color: #A020F0; position: relative; z-index: 10; }
        .ava-preview { width: 100%; height: 100%; object-fit: cover; position: absolute; inset: 0; }

        div[data-testid="stTextInput"] div[data-baseweb="input"] { background: rgba(255, 255, 255, 0.04) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 25px !important; max-width: 350px; margin: 0 auto; }
        div[data-testid="stTextInput"] input { text-align: center !important; color: white !important; }
        div[data-testid="stTextInput"] label { display: none !important; }

        .center-btn { display: flex; justify-content: center; width: 100%; margin-top: 40px; }
        .center-btn button { background: rgba(255, 255, 255, 0.02) !important; border: 1px solid rgba(160, 32, 240, 0.4) !important; border-radius: 50% !important; color: #A020F0 !important; width: 70px !important; height: 70px !important; font-size: 28px !important; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 style="text-align:center; font-weight:800; margin-bottom:40px; margin-top:20px;">cotakbass music</h1>', unsafe_allow_html=True)
    
    # ПРЯМОУГОЛЬНИК
    st.markdown('<div class="upload-wrapper" style="max-width:500px; height:160px;"><div class="bg-draw">+</div>', unsafe_allow_html=True)
    st.file_uploader("bg", key="reg_bg")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # КРУГ
    st.markdown('<div class="upload-wrapper" style="width:130px; height:130px; margin-top:-65px;"><div class="ava-draw">', unsafe_allow_html=True)
    u_ava = st.file_uploader("ava", key="reg_ava")
    img_64 = get_base64_img(u_ava)
    if img_64: st.markdown(f'<img src="data:image/png;base64,{img_64}" class="ava-preview">', unsafe_allow_html=True)
    else: st.write("+")
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    name = st.text_input("name", placeholder="name", key="reg_n")
    bio = st.text_input("status", placeholder="status", key="reg_s")
    
    st.markdown('<div class="center-btn">', unsafe_allow_html=True)
    if st.button("❯"):
        if name:
            st.session_state.auth = True
            st.session_state.user_name = name
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
