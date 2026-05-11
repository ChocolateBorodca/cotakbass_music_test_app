import streamlit as st
import base64

def get_base64_img(file):
    if file: return base64.b64encode(file.getvalue()).decode()
    return None

def registration_screen():
    # Твой уникальный дизайн из рисунка
    st.markdown(f"""
        <style>
        header, footer, #MainMenu, [data-testid="stInputInstructions"] {{ display: none !important; }}
        .stApp {{ background-color: #000000; color: #FFFFFF; font-family: -apple-system, sans-serif; }}
        
        /* Фикс клика: растягиваем невидимый загрузчик на всю фигуру */
        .upload-wrapper {{
            position: relative;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        [data-testid="stFileUploader"] {{
            position: absolute !important;
            inset: 0 !important;
            width: 100% !important;
            height: 100% !important;
            opacity: 0 !important;
            z-index: 500 !important;
            cursor: pointer !important;
        }}
        [data-testid="stFileUploader"] section {{ padding: 0 !important; min-height: 100% !important; }}

        .bg-draw {{ 
            background: rgba(255,255,255,0.03); 
            backdrop-filter: blur(40px); 
            border: 1px solid rgba(255,255,255,0.1); 
            border-radius: 25px; 
            height: 140px; width: 100%; max-width: 480px; 
            display: flex; align-items: center; justify-content: center; 
            font-size: 32px; color: rgba(160, 32, 240, 0.4); 
        }}

        .ava-draw {{ 
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
        }}
        .preview-img {{ width: 100%; height: 100%; object-fit: cover; position: absolute; inset: 0; }}
        
        div[data-testid="stTextInput"] div[data-baseweb="input"] {{ 
            background: rgba(255, 255, 255, 0.04) !important; 
            border-radius: 30px !important; 
            max-width: 350px; margin: 0 auto; 
            border: 1px solid rgba(255,255,255,0.1) !important; 
        }}
        div[data-testid="stTextInput"] input {{ text-align: center !important; color: white !important; }}
        div[data-testid="stTextInput"] label {{ display: none !important; }}

        /* Кнопка стрелка ❯ */
        .door-btn-box {{ display: flex; justify-content: center; margin-top: 30px; }}
        .door-btn-box button {{ 
            background: rgba(255, 255, 255, 0.02) !important; 
            border: 1px solid rgba(160, 32, 240, 0.4) !important; 
            border-radius: 50% !important; 
            color: #A020F0 !important; 
            width: 65px !important; height: 65px !important; 
            font-size: 28px !important; 
        }}
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 style="text-align:center; font-weight:200; margin-top:20px;">cotakbass</h1>', unsafe_allow_html=True)
    
    # Прямоугольник (ФОН)
    st.markdown('<div class="upload-wrapper" style="max-width:480px; height:140px;">', unsafe_allow_html=True)
    st.markdown('<div class="bg-draw">+</div>', unsafe_allow_html=True)
    st.file_uploader("", key="u_bg")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Круг (АВА)
    st.markdown('<div class="upload-wrapper" style="width:120px; height:120px; margin-top:-60px;">', unsafe_allow_html=True)
    st.markdown('<div class="ava-draw">', unsafe_allow_html=True)
    u_ava = st.file_uploader("", key="u_ava")
    base64_ava = get_base64_img(u_ava)
    if base64_ava:
        st.markdown(f'<img src="data:image/png;base64,{base64_ava}" class="preview-img">', unsafe_allow_html=True)
    else:
        st.write("+")
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.write("<div style='height:20px'></div>", unsafe_allow_html=True)
    name = st.text_input("name", placeholder="name", key="reg_n")
    status = st.text_input("status", placeholder="status", key="reg_s")
    
    st.markdown('<div class="door-btn-box">', unsafe_allow_html=True)
    if st.button("❯"):
        if name:
            st.session_state.auth = True
            st.session_state.user_name = name
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
