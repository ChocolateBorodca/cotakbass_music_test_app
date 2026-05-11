import streamlit as st
import os
import random
import base64

st.set_page_config(page_title="cotakbass music", layout="wide", initial_sidebar_state="collapsed")

# Папки
MUSIC_DIR = "music"
BG_DIR = "bg"
for d in [MUSIC_DIR, BG_DIR]:
    if not os.path.exists(d): os.makedirs(d)

tracks = sorted([f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")])
bg_gifs = [f for f in os.listdir(BG_DIR) if f.endswith(".gif")]

# Состояния
if 'page' not in st.session_state: st.session_state.page = "main"
if 'track_index' not in st.session_state: st.session_state.track_index = 0
if 'favorites' not in st.session_state: st.session_state.favorites = set()
if 'playing' not in st.session_state: st.session_state.playing = False
if 'current_bg' not in st.session_state: st.session_state.current_bg = None

ICON_URL = "https://githubusercontent.com"

# Логика фона
bg_html = ""
if st.session_state.playing and bg_gifs:
    if st.session_state.current_bg is None:
        st.session_state.current_bg = random.choice(bg_gifs)
    try:
        with open(os.path.join(BG_DIR, st.session_state.current_bg), "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()
        bg_html = f'background-image: url("data:image/gif;base64,{encoded}"); background-size: cover; background-position: center;'
    except:
        bg_html = "background-color: #000000;"
else:
    st.session_state.current_bg = None
    bg_html = "background-color: #000000;"

# Стили
st.markdown(f"""
    <style>
    header, footer, .stDeployButton, #MainMenu {{visibility: hidden !important;}}
    html, body, [class*="st-"] {{ font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important; }}
    .stApp {{ {bg_html} transition: background 0.8s ease-in-out; }}
    .stApp::before {{ content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.7); z-index: -1; }}
    audio {{ display: none !important; }}
    .app-header {{ font-size: 12px; font-weight: 600; letter-spacing: 3px; text-transform: lowercase; color: #A020F0; text-align: center; margin-bottom: 20px; }}
    .track-title {{ font-size: clamp(30px, 8vw, 48px); font-weight: 700; text-align: center; margin-top: 20px; line-height: 1.2; }}
    .track-author {{ font-size: 18px; color: #A020F0; margin-bottom: 50px; text-align: center; opacity: 0.8; }}

    /* Стеклянные кнопки */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(160, 32, 240, 0.3) !important;
        border-radius: 50% !important;
        color: white !important;
        width: 60px !important; height: 60px !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        margin: auto !important;
    }}
    /* Поле поиска (стекло) */
    div[data-testid="stTextInput"] input {{
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(160, 32, 240, 0.3) !important;
        border-radius: 20px !important;
        color: white !important;
        backdrop-filter: blur(10px);
    }}
    </style>
    """, unsafe_allow_html=True)

# Навигация: Библиотека (Слева) | Поиск (Справа)
nav_l, _, nav_r = st.columns([1, 4, 1])
with nav_l:
    if st.button("←" if st.session_state.page != "main" else "☰"):
        st.session_state.page = "main" if st.session_state.page != "main" else "library"
        st.rerun()
with nav_r:
    if st.button("🔍"):
        st.session_state.page = "search"
        st.rerun()

if not tracks:
    st.info("No tracks in /music")
else:
    # --- ЭКРАН ПОИСКА ---
    if st.session_state.page == "search":
        st.markdown('<div class="app-header">search</div>', unsafe_allow_html=True)
        search_query = st.text_input("", placeholder="Найти трек или автора...")
        if search_query:
            results = [t for t in tracks if search_query.lower() in t.lower()]
            for res in results:
                if st.button(f"🎵 {res.replace('.mp3', '')}", key=f"search_{res}", use_container_width=True):
                    st.session_state.track_index = tracks.index(res)
                    st.session_state.page = "main"
                    st.session_state.playing = True
                    st.rerun()

    # --- ЭКРАН БИБЛИОТЕКИ ---
    elif st.session_state.page == "library":
        st.markdown('<div class="app-header">favorites</div>', unsafe_allow_html=True)
        for fav in list(st.session_state.favorites):
            col_t, col_b = st.columns([0.8, 0.2])
            with col_t: st.markdown(f"<div style='padding:15px 0; border-bottom:1px solid #222;'>{fav.replace('.mp3', '')}</div>", unsafe_allow_html=True)
            with col_b:
                if st.button("▶", key=f"f_{fav}"):
                    st.session_state.track_index = tracks.index(fav)
                    st.session_state.page = "main"
                    st.session_state.playing = True
                    st.rerun()

    # --- ГЛАВНЫЙ ЭКРАН ---
    else:
        current_file = tracks[st.session_state.track_index]
        st.markdown('<div class="app-header">cotakbass music</div>', unsafe_allow_html=True)
        name_clean = current_file.replace(".mp3", "").replace("_", " ")
        author, title = name_clean.split(", ", 1) if ", " in name_clean else ("unknown", name_clean)
        st.markdown(f'<div class="track-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="track-author">{author}</div>', unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("❮"):
                st.session_state.track_index = (st.session_state.track_index - 1) % len(tracks)
                st.session_state.current_bg = None
                st.rerun()
        with c2:
            icon = "Ⅱ" if st.session_state.playing else "▶"
            if st.button(icon):
                st.session_state.playing = not st.session_state.playing
                st.rerun()
        with c3:
            if st.button("❯"):
                st.session_state.track_index = (st.session_state.track_index + 1) % len(tracks)
                st.session_state.current_bg = None
                st.rerun()
        with c4:
            is_fav = current_file in st.session_state.favorites
            if st.button("💜" if is_fav else "🤍"):
                if is_fav: st.session_state.favorites.remove(current_file)
                else: 
                    st.session_state.favorites.add(current_file)
                    st.snow()
                st.rerun()

    # Движок
    st.audio(os.path.join(MUSIC_DIR, tracks[st.session_state.track_index]), autoplay=st.session_state.playing)
