import streamlit as st
import base64
import os

def get_base_64(file):
    if file: return base64.b64encode(file.getvalue()).decode()
    return None

def registration_screen():
    st.markdown("""
        <style>
        header, footer, #MainMenu, [data-testid="stInputInstructions"] { display: none !important; }
        .stApp { background-color: #000000; color: white; }
        .upload-wrapper { position: relative; margin: 0 auto; display: flex; align-items: center; justify-content: center; }
        [data-testid="stFileUploader"] { position: absolute !important; inset: 0 !important; opacity: 0 !important; z-index: 1000 !important; cursor: pointer !important; }
        .bg-draw { background: rgba(255,255,255,0.03); backdrop-filter: blur(40px); border: 1px solid rgba(255,255,255,0.1); border-radius: 30px; height: 160px; width: 100%; max-width: 500px; display: flex; align-items: center; justify-content: center; font-size: 30px; color: rgba(160, 32, 240, 0.4); }
        .ava-draw { width: 130px; height: 130px; background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(30px); border: 2px solid #A020F0; border-radius: 50%; margin-top: -65px; overflow: hidden; display: flex; align-items: center; justify-content: center; font-size: 30px; color: #A020F0; position: relative; z-index: 10; }
        .ava-preview { width: 100%; height: 100%; object-fit: cover; position: absolute; }
        div[data-testid="stTextInput"] div[data-baseweb="input"] { background: rgba(255, 255, 255, 0.04) !important; border-radius: 25px !important; max-width: 350px; margin: 0 auto; }
        div[data-testid="stTextInput"] input { text-align: center !important; color: white !important; }
        .center-btn { display: flex; justify-content: center; width: 100%; margin-top: 30px; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 style="text-align:center; font-weight:200;">registration</h1>', unsafe_allow_html=True)
    
    # Прямоугольник (ФОН)
    st.markdown('<div class="upload-wrapper" style="max-width:500px; height:160px;"><div class="bg-draw">+</div>', unsafe_allow_html=True)
    st.file_uploader("bg", key="reg_bg")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Круг (АВА)
    st.markdown('<div class="upload-wrapper" style="width:130px; height:130px; margin-top:-65px;"><div class="ava-draw">', unsafe_allow_html=True)
    u_ava = st.file_uploader("ava", key="reg_ava")
    img_64 = get_base_64(u_ava)
    if img_64: 
        st.markdown(f'<img src="data:image/png;base64,{img_64}" class="ava-preview">', unsafe_allow_html=True)
        st.session_state.user['ava'] = img_64
    else: st.write("+")
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    name = st.text_input("", placeholder="name", key="reg_n")
    bio = st.text_input("", placeholder="status", key="reg_s")
    
    st.markdown('<div class="center-btn">', unsafe_allow_html=True)
    if st.button("❯"):
        if name:
            st.session_state.auth = True
            st.session_state.user['name'] = name
            st.session_state.user['bio'] = bio
            st.session_state.page = "main"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def profile_screen():
    # SOUNDCLOUD STYLE PROFILE
    ava_data = st.session_state.user.get('ava')
    name = st.session_state.user.get('name', 'User')
    bio = st.session_state.user.get('bio', '')
    
    st.markdown(f"""
        <style>
        .sc-profile-header {{ position: relative; width: 100%; height: 250px; background: #111; border-radius: 20px; overflow: hidden; margin-bottom: 20px; }}
        .sc-avatar {{ position: absolute; bottom: 20px; left: 20px; width: 150px; height: 150px; border-radius: 50%; border: 3px solid #A020F0; box-shadow: 0 0 20px rgba(160, 32, 240, 0.5); object-fit: cover; }}
        .sc-info {{ position: absolute; bottom: 40px; left: 190px; color: white; }}
        .sc-name {{ font-size: 32px; font-weight: 800; }}
        .sc-bio {{ font-size: 16px; opacity: 0.7; }}
        </style>
        <div class="sc-profile-header">
            <img class="sc-avatar" src="data:image/png;base64,{ava_data if ava_data else ''}">
            <div class="sc-info">
                <div class="sc-name">{name}</div>
                <div class="sc-bio">{bio}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("Опубликовать трек")
    up_track = st.file_uploader("выбери mp3", type="mp3")
    t_name = st.text_input("название трека")
    
    if st.button("Опубликовать") and up_track and t_name:
        with open(os.path.join("music", f"{name} - {t_name}.mp3"), "wb") as f:
            f.write(up_track.getbuffer())
        st.success("Трек опубликован!")
    
    if st.button("← Назад в плеер"):
        st.session_state.page = "main"
        st.rerun()
