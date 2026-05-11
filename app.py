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
    except: bg_html = "background-color: #000000;"
else:
    st.session_state.current_bg = None
    bg_html = "background-color: #000000;"

# УЛЬТРА-CSS: Ломаем стандартные стили Streamlit для поиска
st.markdown(f"""
    <style>
    header, footer, .stDeployButton, #MainMenu {{visibility: hidden !important;}}
    html, body, [class*="st-"] {{ font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important; }}
    .stApp {{ {bg_html} transition: background 0.8s ease-in-out; }}
    .stApp::before {{ content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.75); z-index: -1; }}
    audio {{ display: none !important; }}
    
    .app-header {{ font-size: 11px; font-weight: 600; letter-spacing: 3px; text-transform: lowercase; color: #A020F0; text-align: center; margin-bottom: 30px; }}

    /* Стеклянные кнопки управления */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(160, 32, 240, 0.2) !important;
        border-radius: 50% !important;
        color: white !important;
        width: 60px !important; height: 60px !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        margin: auto !important;
    }}

    /* ПОЛНОСТЬЮ СТЕКЛЯННЫЙ ПОИСК */
    div[data-testid="stTextInput"] {{
        background: transparent !important;
    }}
    div[data-testid="stTextInput"] div[data-baseweb="input"] {{
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        color: white !important;
    }}
    div[data-testid="stTextInput"] input {{
        background: transparent !important;
        color: white !important;
        padding: 15px !important;
        border: none !important;
    }}
    div[data-testid="stTextInput"] label {{ display: none !important; }}

    /* Кнопки в списке */
    .track-row-custom {{
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.05);
    }}
    </style>
    """, unsafe_allow_html=True)

# Навигация (Библиотека | Поиск)
nav_l, _, nav_r = st.columns([0.2, 0.6, 0.2])
with nav_l:
    if st.button("←" if st.session_state.page != "main" else "☰"):
        st.session_state.page = "main" if st.session_state.page != "main" else "library"
        st.rerun()
with nav_r:
    if st.button("○"): # Заменили лупу на круг
        st.session_state.page = "search"
        st.rerun()

if not tracks:
    st.info("No tracks in /music")
else:
    # --- ЭКРАН ПОИСКА ---
    if st.session_state.page == "search":
        st.markdown('<div class="app-header">search</div>', unsafe_allow_html=True)
        # Обработка Enter реализована через стандартный механизм Streamlit
        query = st.text_input("", placeholder="Напечатай и нажми Enter...", key="search_input")
        
        if query:
            filtered = [t for t in tracks if query.lower() in t.lower()]
            if not filtered:
                st.write("<p style='text-align:center; opacity:0.5;'>Ничего не найдено</p>", unsafe_allow_html=True)
            for track in filtered:
                c_name, c_play = st.columns([0.8, 0.2])
                with c_name:
                    st.markdown(f"<div style='padding-top:18px; font-size:16px;'>{track.replace('.mp3', '')}</div>", unsafe_allow_html=True)
                with c_play:
                    if st.button("▶", key=f"s_{track}"):
                        st.session_state.track_index = tracks.index(track)
                        st.session_state.page = "main"
                        st.session_state.playing = True
                        st.rerun()

    # --- ЭКРАН БИБЛИОТЕКИ ---
    elif st.session_state.page == "library":
        st.markdown('<div class="app-header">favorites</div>', unsafe_allow_html=True)
        if not st.session_state.favorites:
            st.write("<p style='text-align:center; opacity:0.5;'>Пусто</p>", unsafe_allow_html=True)
        else:
            for fav in list(st.session_state.favorites):
                c_name, c_play = st.columns([0.8, 0.2])
                with c_name:
                    st.markdown(f"<div style='padding-top:18px; font-size:16px; border-bottom:1px solid #111;'>{fav.replace('.mp3', '')}</div>", unsafe_allow_html=True)
                with c_play:
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
        
        st.markdown(f'<div style="text-align:center; margin-top:5vh;">', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:42px; font-weight:700; margin-bottom:5px;">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:18px; color:#A020F0; margin-bottom:60px;">{author}</div>', unsafe_allow_html=True)
        
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
        st.markdown('</div>', unsafe_allow_html=True)

    st.audio(os.path.join(MUSIC_DIR, tracks[st.session_state.track_index]), autoplay=st.session_state.playing)
