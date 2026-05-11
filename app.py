import streamlit as st
import os
import random
import base64

# Ультра-настройка страницы
st.set_page_config(
    page_title="cotakbass music", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Папки
MUSIC_DIR = "music"
BG_DIR = "bg"
for d in [MUSIC_DIR, BG_DIR]:
    if not os.path.exists(d): os.makedirs(d)

tracks = sorted([f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")])
bg_gifs = [f for f in os.listdir(BG_DIR) if f.endswith(".gif")]

# Инициализация
if 'page' not in st.session_state: st.session_state.page = "main"
if 'track_index' not in st.session_state: st.session_state.track_index = 0
if 'favorites' not in st.session_state: st.session_state.favorites = set()
if 'playing' not in st.session_state: st.session_state.playing = False
if 'current_bg' not in st.session_state: st.session_state.current_bg = None

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

# УЛЬТРА-CSS (Убираем Streamlit по максимуму)
st.markdown(f"""
    <style>
    /* Прячем всё стандартное */
    header, footer, .stDeployButton, #MainMenu {{visibility: hidden !important;}}
    [data-testid="stHeader"] {{background: rgba(0,0,0,0) !important;}}
    .block-container {{padding: 1rem 1rem !important;}}
    
    html, body, [class*="st-"] {{
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important;
        background-color: #000000;
    }}
    
    .stApp {{
        {bg_style}
        transition: background 0.8s ease;
    }}
    
    .stApp::before {{
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.75); z-index: -1;
    }}
    
    audio {{ display: none !important; }}
    
    .app-header {{
        font-size: 11px; font-weight: 600; letter-spacing: 4px;
        text-transform: lowercase; color: #A020F0;
        margin-top: 10px; margin-bottom: 30px; text-align: center; opacity: 0.7;
    }}
    
    .track-title {{ 
        font-size: clamp(32px, 9vw, 52px); font-weight: 800; 
        letter-spacing:-2px; text-align: center; margin-top: 40px;
        line-height: 1.1;
    }}
    
    .track-author {{ 
        font-size: clamp(16px, 5vw, 22px); color:#A020F0; 
        margin-bottom: 60px; opacity:0.9; text-align: center;
        font-weight: 300;
    }}

    /* Кнопки управления */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(25px) !important;
        border: 1px solid rgba(160, 32, 240, 0.15) !important;
        border-radius: 50% !important;
        color: white !important;
        width: 70px !important; height: 70px !important;
        display: flex; align-items: center; justify-content: center;
        transition: 0.2s ease !important;
        margin: auto;
    }}
    
    div.stButton > button:active {{
        transform: scale(0.9) !important;
        background: rgba(160, 32, 240, 0.2) !important;
    }}

    /* Ссылки на иконки */
    <link rel="apple-touch-icon" href="{ICON_URL}">
    <link rel="icon" href="{ICON_URL}">
    </style>
    """, unsafe_allow_html=True)

# Верхняя навигация
c_nav, _ = st.columns([0.2, 0.8])
with c_nav:
    if st.button("←" if st.session_state.page == "library" else "☰"):
        st.session_state.page = "library" if st.session_state.page == "main" else "main"
        st.rerun()

if not tracks:
    st.info("No tracks in /music")
else:
    current_file = tracks[st.session_state.track_index]

    if st.session_state.page == "library":
        st.markdown('<div class="app-header">favorites</div>', unsafe_allow_html=True)
        for fav in list(st.session_state.favorites):
            col_t, col_b = st.columns([0.8, 0.2])
            with col_t: st.markdown(f"<div style='padding:15px 0; font-size:18px; border-bottom:1px solid #111;'>{fav.replace('.mp3', '')}</div>", unsafe_allow_html=True)
            with col_b:
                if st.button("▶", key=f"f_{fav}"):
                    st.session_state.track_index = tracks.index(fav)
                    st.session_state.page = "main"
                    st.session_state.playing = True
                    st.rerun()
    else:
        # Плеер
        st.markdown('<div class="app-header">cotakbass music</div>', unsafe_allow_html=True)
        
        name_clean = current_file.replace(".mp3", "").replace("_", " ")
        author, title = name_clean.split(", ", 1) if ", " in name_clean else ("unknown", name_clean)
        
        st.markdown(f'<div class="track-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="track-author">{author}</div>', unsafe_allow_html=True)
        
        # Кнопки
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
