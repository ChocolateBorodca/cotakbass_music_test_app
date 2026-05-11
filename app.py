import streamlit as st
import os
import random
import base64

# Конфигурация приложения
st.set_page_config(page_title="cotakbass music", layout="wide", initial_sidebar_state="collapsed")

# Папки
MUSIC_DIR = "music"
BG_DIR = "bg"
for d in [MUSIC_DIR, BG_DIR]:
    if not os.path.exists(d): os.makedirs(d)

tracks = sorted([f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")])
bg_gifs = [f for f in os.listdir(BG_DIR) if f.endswith(".gif")]

# Инициализация состояний
if 'page' not in st.session_state: st.session_state.page = "main"
if 'track_index' not in st.session_state: st.session_state.track_index = 0
if 'favorites' not in st.session_state: st.session_state.favorites = set()
if 'playing' not in st.session_state: st.session_state.playing = False
if 'current_bg' not in st.session_state: st.session_state.current_bg = None

# Твоя новая PNG ссылка (с обходом кэша)
ICON_URL = "https://githubusercontent.com"

# Логика GIF-фона
bg_style = ""
if st.session_state.playing and bg_gifs:
    if st.session_state.current_bg is None:
        st.session_state.current_bg = random.choice(bg_gifs)
    try:
        with open(os.path.join(BG_DIR, st.session_state.current_bg), "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()
        bg_style = f'background-image: url("data:image/gif;base64,{encoded}"); background-size: cover; background-position: center;'
    except:
        bg_style = "background-color: #000000;"
else:
    st.session_state.current_bg = None
    bg_style = "background-color: #000000;"

# Ультра-дизайн и скрытые мета-теги
st.markdown(f"""
    <style>
    html, body, [class*="st-"] {{
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important;
    }}
    .stApp {{
        {bg_style}
        transition: background 1s ease-in-out;
    }}
    .stApp::before {{
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.75); z-index: -1;
    }}
    audio {{ display: none !important; }}
    
    .app-header {{
        font-size: 12px; font-weight: 500; letter-spacing: 3px;
        text-transform: lowercase; color: #A020F0;
        margin-bottom: 20px; text-align: center; opacity: 0.8;
    }}
    
    .track-title {{ 
        font-size: clamp(28px, 8vw, 48px); font-weight: 700; 
        letter-spacing:-1.5px; text-align: center; margin-top: 20px;
    }}
    .track-author {{ 
        font-size: clamp(16px, 4vw, 20px); color:#A020F0; 
        margin-bottom: 50px; opacity:0.8; text-align: center;
    }}

    div.stButton > button {{
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(160, 32, 240, 0.2) !important;
        border-radius: 50% !important;
        color: white !important;
        width: 65px !important; height: 65px !important;
        display: flex; align-items: center; justify-content: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin: auto;
    }}
    
    div.stButton > button:active {{ transform: scale(0.9); }}
    
    header {{visibility: hidden;}}
    </style>
    
    <link rel="apple-touch-icon" href="{ICON_URL}">
    <link rel="icon" type="image/png" href="{ICON_URL}">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    """, unsafe_allow_html=True)

# Кнопка Библиотеки
nav_c, _ = st.columns([0.2, 0.8])
with nav_c:
    if st.button("←" if st.session_state.page == "library" else "☰"):
        st.session_state.page = "library" if st.session_state.page == "main" else "main"
        st.rerun()

if not tracks:
    st.info("Добавь музыку в music/")
else:
    current_file = tracks[st.session_state.track_index]

    if st.session_state.page == "library":
        st.markdown('<div class="app-header">favorites</div>', unsafe_allow_html=True)
        if not st.session_state.favorites:
            st.write("<p style='text-align:center; opacity:0.5;'>Тут пусто</p>", unsafe_allow_html=True)
        else:
            for fav in list(st.session_state.favorites):
                col_t, col_b = st.columns([0.75, 0.25])
                with col_t: st.markdown(f"<div style='padding-top:15px; font-size:16px;'>{fav.replace('.mp3', '').replace('_', ' ')}</div>", unsafe_allow_html=True)
                with col_b:
                    if st.button("▶", key=f"fav_play_{fav}"):
                        st.session_state.track_index = tracks.index(fav)
                        st.session_state.page = "main"
                        st.session_state.playing = True
                        st.rerun()
    else:
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
            if st.button("Ⅱ" if st.session_state.playing else "▶"):
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

    st.audio(os.path.join(MUSIC_DIR, current_file), autoplay=st.session_state.playing)
