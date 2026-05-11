import streamlit as st
import os
import random
import base64

st.set_page_config(page_title="cotakbass music", layout="wide", initial_sidebar_state="collapsed")

# Настройки папок
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

# МАГИЯ CSS: Матовое стекло и скрытие инструкций
st.markdown(f"""
    <style>
    header, footer, .stDeployButton, #MainMenu {{visibility: hidden !important;}}
    html, body, [class*="st-"] {{ font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important; }}
    
    .stApp {{ {bg_html} transition: background 0.8s ease; }}
    .stApp::before {{ content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.85); z-index: -1; }}
    audio {{ display: none !important; }}
    
    /* Стеклянные кнопки навигации */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(30px) !important;
        -webkit-backdrop-filter: blur(30px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 50% !important;
        color: white !important;
        width: 50px !important; height: 50px !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        transition: 0.3s ease !important;
        margin: auto !important;
    }}

    /* УЛЬТРА-МАТОВЫЙ ПОИСК */
    div[data-testid="stTextInput"] div[data-baseweb="input"] {{
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(50px) brightness(0.8) !important;
        -webkit-backdrop-filter: blur(50px) brightness(0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        position: relative;
    }}
    
    /* Имитация лупы внутри поиска */
    div[data-testid="stTextInput"] div[data-baseweb="input"]::after {{
        content: "🔍";
        position: absolute;
        right: 20px;
        top: 50%;
        transform: translateY(-50%);
        opacity: 0.5;
        font-size: 18px;
    }}

    div[data-testid="stTextInput"] input {{
        color: white !important;
        padding: 20px 50px 20px 20px !important;
    }}
    
    /* Скрытие "Press Enter" */
    div[data-testid="stInputInstructions"] {{ display: none !important; }}
    div[data-testid="stTextInput"] label {{ display: none !important; }}

    .track-info {{ font-size: 16px; font-weight: 300; padding-top: 15px; border-bottom: 1px solid rgba(255,255,255,0.05); }}
    .app-header {{ font-size: 10px; letter-spacing: 4px; text-transform: lowercase; color: #A020F0; text-align: center; margin-bottom: 40px; opacity: 0.6; }}
    </style>
    """, unsafe_allow_html=True)

# Навигация
n1, _, n2 = st.columns([0.15, 0.7, 0.15])
with n1:
    if st.button("←" if st.session_state.page != "main" else "☰"):
        st.session_state.page = "main" if st.session_state.page != "main" else "library"
        st.rerun()
with n2:
    if st.button("🔍"):
        st.session_state.page = "search"
        st.rerun()

if not tracks:
    st.info("No tracks")
else:
    # --- ЭКРАН ПОИСКА ---
    if st.session_state.page == "search":
        st.markdown('<div class="app-header">search</div>', unsafe_allow_html=True)
        query = st.text_input("", placeholder="напиши хуйню", key="search_input")
        
        if query:
            filtered = [t for t in tracks if query.lower() in t.lower()]
            for track in filtered:
                c_name, c_play = st.columns([0.85, 0.15])
                with c_name:
                    st.markdown(f"<div class='track-info'>{track.replace('.mp3', '')}</div>", unsafe_allow_html=True)
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
                c_name, c_play = st.columns([0.85, 0.15])
                with c_name:
                    st.markdown(f"<div class='track-info'>{fav.replace('.mp3', '')}</div>", unsafe_allow_html=True)
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
        
        st.markdown(f'<div style="text-align:center; margin-top:8vh;">', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:42px; font-weight:700; margin-bottom:5px;">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:18px; color:#A020F0; margin-bottom:60px;">{author}</div>', unsafe_allow_html=True)
        
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
        st.markdown('</div>', unsafe_allow_html=True)

    st.audio(os.path.join(MUSIC_DIR, tracks[st.session_state.track_index]), autoplay=st.session_state.playing)
