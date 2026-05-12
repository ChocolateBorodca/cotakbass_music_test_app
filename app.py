import streamlit as st
import os
import random
import base64

# --- 1. НАСТРОЙКИ ---
st.set_page_config(page_title="cotakbass music", layout="wide", initial_sidebar_state="collapsed")

# Папки
for d in ["music", "bg", "avatars"]:
    if not os.path.exists(d): os.makedirs(d)

# Session State
if 'page' not in st.session_state: st.session_state.page = "main"
if 'track_index' not in st.session_state: st.session_state.track_index = 0
if 'favorites' not in st.session_state: st.session_state.favorites = set()
if 'playing' not in st.session_state: st.session_state.playing = False
if 'current_bg' not in st.session_state: st.session_state.current_bg = None
if 'user_ava' not in st.session_state: st.session_state.user_ava = None

def get_base64(file):
    return base64.b64encode(file.getvalue()).decode() if file else None

# --- 2. ДИНАМИЧЕСКИЙ ФОН ---
bg_css = "background-color: #000000;"
bg_gifs = [f for f in os.listdir("bg") if f.endswith(".gif")]
if st.session_state.playing and bg_gifs:
    if st.session_state.current_bg is None:
        st.session_state.current_bg = random.choice(bg_gifs)
    try:
        with open(os.path.join("bg", st.session_state.current_bg), "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        bg_css = f'background-image: url("data:image/gif;base64,{encoded}"); background-size: cover; background-position: center;'
    except: pass
else:
    st.session_state.current_bg = None

# --- 3. СТИЛИ (APPLE + OLED + CLEAN) ---
st.markdown(f"""
    <style>
    /* Полная зачистка мусора Streamlit и точек */
    header, footer, #MainMenu, [data-testid="stInputInstructions"], 
    .st-emotion-cache-oc994i, .st-emotion-cache-1pxm666, .st-emotion-cache-1vt4y65 {{
        display: none !important;
        visibility: hidden !important;
    }}
    
    html, body, [class*="st-"] {{ font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important; }}
    .stApp {{ {bg_css} transition: background 0.8s ease; }}
    .stApp::before {{ content: ""; position: absolute; inset: 0; background: rgba(0, 0, 0, 0.88); z-index: -1; }}
    audio {{ display: none !important; }}

    /* Кнопки навигации */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(40px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 50% !important;
        color: #A020F0 !important;
        width: 55px !important; height: 55px !important;
        transition: 0.3s ease;
    }}

    /* Специфический стиль для кнопки профиля (свечение если есть ава) */
    .nav-profile-btn button {{ 
        box-shadow: { '0 0 15px #A020F0' if st.session_state.user_ava else 'none' };
        border: { '2px solid #A020F0' if st.session_state.user_ava else '1px solid rgba(255,255,255,0.1)' } !important;
    }}

    /* ЭКРАН ПРОФИЛЯ: КРУГ С ПЛЮСИКОМ */
    .upload-wrapper {{
        position: relative;
        width: 180px; height: 180px;
        margin: 15vh auto;
        display: flex; align-items: center; justify-content: center;
    }}
    [data-testid="stFileUploader"] {{
        position: absolute !important; inset: 0 !important;
        width: 100% !important; height: 100% !important;
        opacity: 0 !important; z-index: 1000 !important;
        cursor: pointer !important;
    }}
    .ava-visual {{
        width: 100%; height: 100%;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(30px);
        border: 2px solid #A020F0;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 50px; color: #A020F0;
        overflow: hidden;
    }}
    .ava-preview-img {{ width: 100%; height: 100%; object-fit: cover; position: absolute; inset: 0; }}

    /* ПЛЕЕР: ТЕКСТ СЛЕВА */
    .track-info-left {{ text-align: left; padding-left: 5%; margin-top: 15vh; }}
    .title-text {{ font-size: clamp(32px, 8vw, 52px); font-weight: 800; color: white; letter-spacing: -2px; line-height: 1; }}
    .author-text {{ font-size: 18px; color: #A020F0; font-weight: 300; margin-top: 8px; margin-bottom: 60px; opacity: 0.8; }}

    /* ПОИСК */
    div[data-testid="stTextInput"] div[data-baseweb="input"] {{ 
        background: rgba(255, 255, 255, 0.03) !important; 
        backdrop-filter: blur(60px) brightness(0.7) !important; 
        border: 1px solid rgba(160, 32, 240, 0.2) !important; 
        border-radius: 22px !important; 
        position: relative; 
    }}
    div[data-testid="stTextInput"] div[data-baseweb="input"]::after {{ 
        content: "?"; position: absolute; right: 20px; top: 50%; transform: translateY(-50%); 
        color: #A020F0; font-weight: 700; font-size: 18px; 
    }}
    div[data-testid="stTextInput"] input {{ color: white !important; background: transparent !important; padding: 20px !important; border: none !important; }}
    .list-item {{ font-size: 16px; font-weight: 300; padding: 18px 0; border-bottom: 1px solid rgba(255,255,255,0.02); color: white; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. ЛОГИКА ЭКРАНОВ ---

# Экран Профиля (Только круг для авы)
if st.session_state.page == "profile":
    st.markdown('<div style="text-align:center; opacity:0.5; font-size:10px; letter-spacing:5px; margin-top:20px;">PROFILE</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="upload-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="ava-visual">', unsafe_allow_html=True)
    u_ava = st.file_uploader("", key="ava_uploader")
    img_data = get_base64(u_ava)
    if img_data:
        st.session_state.user_ava = img_data
    
    if st.session_state.user_ava:
        st.markdown(f'<img src="data:image/png;base64,{st.session_state.user_ava}" class="ava-preview-img">', unsafe_allow_html=True)
    else:
        st.write("+")
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Кнопка назад
    st.markdown('<div style="display:flex; justify-content:center;">', unsafe_allow_html=True)
    if st.button("←"):
        st.session_state.page = "main"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Основной интерфейс
else:
    # Навигация (☰ | 👤 | ?)
    n1, _, n2, n3 = st.columns([0.15, 0.6, 0.12, 0.13])
    with n1:
        if st.button("☰"): st.session_state.page = "library" if st.session_state.page != "library" else "main"; st.rerun()
    with n2:
        st.markdown('<div class="nav-profile-btn">', unsafe_allow_html=True)
        if st.button("👤"): st.session_state.page = "profile"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with n3:
        if st.button("?"): st.session_state.page = "search"; st.rerun()

    tracks = sorted([f for f in os.listdir("music") if f.endswith(".mp3")])

    if st.session_state.page == "search":
        q = st.text_input("", placeholder="напиши хуйню", key="search_q")
        if q and tracks:
            for t in [x for x in tracks if q.lower() in x.lower()]:
                c_n, c_p = st.columns([0.85, 0.15])
                with c_n: st.markdown(f"<div class='list-item'>{t.replace('.mp3','')}</div>", unsafe_allow_html=True)
                with c_p:
                    if st.button("▶", key=f"s_{t}"):
                        st.session_state.track_index, st.session_state.page, st.session_state.playing = tracks.index(t), "main", True; st.rerun()

    elif st.session_state.page == "library":
        st.markdown('<div style="text-align:center; opacity:0.5; font-size:10px; letter-spacing:5px;">FAVORITES</div>', unsafe_allow_html=True)
        for f in list(st.session_state.favorites):
            c_n, c_p = st.columns([0.85, 0.15])
            with c_n: st.markdown(f"<div class='list-item'>{f.replace('.mp3','')}</div>", unsafe_allow_html=True)
            with c_p:
                if st.button("▶", key=f"l_{f}"):
                    st.session_state.track_index, st.session_state.page, st.session_state.playing = tracks.index(f), "main", True; st.rerun()

    else:
        # ПЛЕЕР
        if tracks:
            st.markdown('<div style="text-align:center; opacity:0.5; font-size:10px; letter-spacing:4px; margin-top:20px;">COTAKBASS MUSIC</div>', unsafe_allow_html=True)
            curr = tracks[st.session_state.track_index]
            name_clean = curr.replace(".mp3", "").replace("_", " ")
            auth, title = name_clean.split(", ", 1) if ", " in name_clean else ("unknown", name_clean)
            
            st.markdown(f"""
                <div class="track-info-left">
                    <div class="title-text">{title}</div>
                    <div class="author-text">{auth}</div>
                </div>
            """, unsafe_allow_html=True)
            
            _, b1, b2, b3, b4, _ = st.columns(6)
            with b1:
                if st.button("❮"): st.session_state.track_index = (st.session_state.track_index - 1) % len(tracks); st.session_state.current_bg = None; st.rerun()
            with b2:
                if st.button("Ⅱ" if st.session_state.playing else "▶"): st.session_state.playing = not st.session_state.playing; st.rerun()
            with b3:
                if st.button("❯"): st.session_state.track_index = (st.session_state.track_index + 1) % len(tracks); st.session_state.current_bg = None; st.rerun()
            with b4:
                is_f = curr in st.session_state.favorites
                if st.button("💜" if is_f else "🤍"):
                    if is_f: st.session_state.favorites.remove(curr)
                    else: st.session_state.favorites.add(curr); st.snow()
                    st.rerun()
            st.audio(os.path.join("music", curr), autoplay=st.session_state.playing)
