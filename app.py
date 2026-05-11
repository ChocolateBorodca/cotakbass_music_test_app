import streamlit as st
import os
import random
import base64

# --- НАСТРОЙКИ ---
st.set_page_config(page_title="cotakbass music", layout="wide", initial_sidebar_state="collapsed")

# Папки
MUSIC_DIR, BG_DIR, AVA_DIR = "music", "bg", "avatars"
for d in [MUSIC_DIR, BG_DIR, AVA_DIR]:
    if not os.path.exists(d): os.makedirs(d)

# Данные
tracks = sorted([f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")])
bg_gifs = [f for f in os.listdir(BG_DIR) if f.endswith(".gif")]

# Session State
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user' not in st.session_state: st.session_state.user = {"name": "", "bio": "", "ava": None}
if 'page' not in st.session_state: st.session_state.page = "main"
if 'track_index' not in st.session_state: st.session_state.track_index = 0
if 'favorites' not in st.session_state: st.session_state.favorites = set()
if 'playing' not in st.session_state: st.session_state.playing = False
if 'current_bg' not in st.session_state: st.session_state.current_bg = None

def get_base64(file):
    return base64.b64encode(file.getvalue()).decode() if file else None

# Логика фона
bg_css = "background-color: #000000;"
if st.session_state.playing and bg_gifs:
    if st.session_state.current_bg is None: st.session_state.current_bg = random.choice(bg_gifs)
    try:
        with open(os.path.join(BG_DIR, st.session_state.current_bg), "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        bg_css = f'background-image: url("data:image/gif;base64,{encoded}"); background-size: cover; background-position: center;'
    except: pass

# --- СТИЛИ ---
st.markdown(f"""
    <style>
    header, footer, #MainMenu, [data-testid="stInputInstructions"], .st-emotion-cache-oc994i {{ display: none !important; }}
    html, body, [class*="st-"] {{ font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important; }}
    .stApp {{ {bg_css} transition: background 0.8s ease; }}
    .stApp::before {{ content: ""; position: absolute; inset: 0; background: rgba(0, 0, 0, 0.85); z-index: -1; }}

    /* Загрузчики (невидимые поверх фигур) */
    .upload-wrapper {{ position: relative; margin: 0 auto; display: flex; align-items: center; justify-content: center; }}
    [data-testid="stFileUploader"] {{ position: absolute !important; inset: 0 !important; opacity: 0 !important; z-index: 100 !important; cursor: pointer !important; }}
    
    /* Фигуры регистрации */
    .bg-draw {{ background: rgba(255,255,255,0.03); backdrop-filter: blur(40px); border: 1px solid rgba(255,255,255,0.1); border-radius: 30px; height: 160px; width: 100%; max-width: 500px; display: flex; align-items: center; justify-content: center; font-size: 30px; color: rgba(160, 32, 240, 0.4); }}
    .ava-draw {{ width: 130px; height: 130px; background: rgba(255,255,255,0.05); backdrop-filter: blur(30px); border: 2px solid #A020F0; border-radius: 50%; margin-top: -65px; overflow: hidden; display: flex; align-items: center; justify-content: center; font-size: 30px; color: #A020F0; position: relative; z-index: 10; }}
    .ava-preview {{ width: 100%; height: 100%; object-fit: cover; position: absolute; }}

    /* Плеер и Кнопки */
    div.stButton > button {{ background: rgba(255,255,255,0.02) !important; backdrop-filter: blur(30px) !important; border: 1px solid rgba(160,32,240,0.3) !important; border-radius: 50% !important; color: #A020F0 !important; width: 60px !important; height: 60px !important; transition: 0.3s !important; }}
    div.stButton > button:hover {{ transform: scale(1.1); border-color: #A020F0 !important; }}
    
    /* Поля ввода */
    div[data-testid="stTextInput"] div[data-baseweb="input"] {{ background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 25px !important; max-width: 350px; margin: 0 auto; }}
    div[data-testid="stTextInput"] input {{ text-align: center !important; color: white !important; }}
    div[data-testid="stTextInput"] label {{ display: none !important; }}
    </style>
""", unsafe_allow_html=True)

# --- ЛОГИКА ---

if not st.session_state.auth:
    # ЭКРАН РЕГИСТРАЦИИ
    st.markdown('<h1 style="text-align:center; font-weight:800; margin-bottom:40px;">cotakbass music</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="upload-wrapper" style="max-width:500px; height:160px;"><div class="bg-draw">+</div>', unsafe_allow_html=True)
    st.file_uploader("bg", key="u_bg")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="upload-wrapper" style="width:130px; height:130px; margin-top:-65px;"><div class="ava-draw">', unsafe_allow_html=True)
    u_ava = st.file_uploader("ava", key="u_ava")
    base64_ava = get_base64(u_ava)
    if base64_ava: st.markdown(f'<img src="data:image/png;base64,{base64_ava}" class="ava-preview">', unsafe_allow_html=True)
    else: st.write("+")
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    u_name = st.text_input("name", placeholder="name")
    u_bio = st.text_input("status", placeholder="status")
    
    st.markdown('<div style="display:flex; justify-content:center; margin-top:30px;">', unsafe_allow_html=True)
    if st.button("❯"):
        if u_name:
            st.session_state.auth, st.session_state.user['name'] = True, u_name
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # ГЛАВНЫЙ ЭКРАН ПЛЕЕРА
    n1, _, n2 = st.columns([0.15, 0.7, 0.15])
    with n1:
        if st.button("☰"): st.session_state.page = "library"; st.rerun()
    with n2:
        if st.button("?"): st.session_state.page = "search"; st.rerun()

    if not tracks:
        st.info("No tracks in /music")
    else:
        if st.session_state.page == "search":
            st.markdown('<div style="text-align:center; letter-spacing:5px; opacity:0.5;">SEARCH</div>', unsafe_allow_html=True)
            q = st.text_input("", placeholder="напиши хуйню", key="s_q")
            if q:
                for t in [x for x in tracks if q.lower() in x.lower()]:
                    c_t, c_p = st.columns([0.85, 0.15])
                    with c_t: st.markdown(f"<div style='padding:15px 0; border-bottom:1px solid #111;'>{t.replace('.mp3','')}</div>", unsafe_allow_html=True)
                    with c_p:
                        if st.button("▶", key=f"s_{t}"):
                            st.session_state.track_index, st.session_state.page, st.session_state.playing = tracks.index(t), "main", True
                            st.rerun()

        elif st.session_state.page == "library":
            st.markdown('<div style="text-align:center; letter-spacing:5px; opacity:0.5;">FAVORITES</div>', unsafe_allow_html=True)
            for f in list(st.session_state.favorites):
                c_t, c_p = st.columns([0.85, 0.15])
                with c_t: st.markdown(f"<div style='padding:15px 0; border-bottom:1px solid #111;'>{f.replace('.mp3','')}</div>", unsafe_allow_html=True)
                with c_p:
                    if st.button("▶", key=f"l_{f}"):
                        st.session_state.track_index, st.session_state.page, st.session_state.playing = tracks.index(f), "main", True
                        st.rerun()
        
        else:
            # ПЛЕЕР
            st.markdown('<div style="text-align:center; opacity:0.5; font-size:10px; letter-spacing:4px;">COTAKBASS MUSIC</div>', unsafe_allow_html=True)
            curr = tracks[st.session_state.track_index]
            name_c = curr.replace(".mp3", "").replace("_", " ")
            auth, title = name_c.split(", ", 1) if ", " in name_c else ("unknown", name_c)
            
            st.markdown(f'<div style="text-align:center; margin-top:10vh;"><div style="font-size:42px; font-weight:700;">{title}</div><div style="color:#A020F0; font-size:18px; margin-bottom:50px;">{auth}</div></div>', unsafe_allow_html=True)
            
            _, c1, c2, c3, c4, _ = st.columns(6)
            with c1:
                if st.button("❮"): st.session_state.track_index = (st.session_state.track_index - 1) % len(tracks); st.session_state.current_bg = None; st.rerun()
            with c2:
                if st.button("Ⅱ" if st.session_state.playing else "▶"): st.session_state.playing = not st.session_state.playing; st.rerun()
            with c3:
                if st.button("❯"): st.session_state.track_index = (st.session_state.track_index + 1) % len(tracks); st.session_state.current_bg = None; st.rerun()
            with c4:
                is_f = curr in st.session_state.favorites
                if st.button("💜" if is_f else "🤍"):
                    if is_f: st.session_state.favorites.remove(curr)
                    else: st.session_state.favorites.add(curr); st.snow()
                    st.rerun()
        
        st.audio(os.path.join(MUSIC_DIR, tracks[st.session_state.track_index]), autoplay=st.session_state.playing)
