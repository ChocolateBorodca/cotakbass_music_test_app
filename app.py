import streamlit as st
import os
import random
import base64
from components.auth import registration_screen # Импорт из новой папки

# Настройка
st.set_page_config(page_title="cotakbass music", layout="wide", initial_sidebar_state="collapsed")

# Папки
MUSIC_DIR, BG_DIR = "music", "bg"
for d in [MUSIC_DIR, BG_DIR]:
    if not os.path.exists(d): os.makedirs(d)

# Session State
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'page' not in st.session_state: st.session_state.page = "main"
if 'track_index' not in st.session_state: st.session_state.track_index = 0
if 'favorites' not in st.session_state: st.session_state.favorites = set()
if 'playing' not in st.session_state: st.session_state.playing = False
if 'current_bg' not in st.session_state: st.session_state.current_bg = None

# --- ЛОГИКА ЗАПУСКА ---

if not st.session_state.auth:
    # Вызываем экран из отдельной папки
    registration_screen()
else:
    # ТВОЙ ИДЕАЛЬНЫЙ ПЛЕЕР (Код плеера)
    tracks = sorted([f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")])
    bg_gifs = [f for f in os.listdir(BG_DIR) if f.endswith(".gif")]

    bg_html = "background-color: #000000;"
    if st.session_state.playing and bg_gifs:
        if st.session_state.current_bg is None:
            st.session_state.current_bg = random.choice(bg_gifs)
        try:
            with open(os.path.join(BG_DIR, st.session_state.current_bg), "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            bg_html = f'background-image: url("data:image/gif;base64,{encoded}"); background-size: cover; background-position: center;'
        except: pass

    st.markdown(f"""
        <style>
        header, footer, #MainMenu, [data-testid="stInputInstructions"], .st-emotion-cache-1pxm666 {{ display: none !important; }}
        .stApp {{ {bg_html} transition: background 0.8s ease; }}
        .stApp::before {{ content: ""; position: absolute; inset: 0; background: rgba(0, 0, 0, 0.85); z-index: -1; }}
        audio {{ display: none !important; }}
        div.stButton > button {{ background: rgba(255, 255, 255, 0.02) !important; backdrop-filter: blur(30px) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 50% !important; color: white !important; width: 55px !important; height: 55px !important; transition: 0.3s ease; }}
        .search-title {{ font-size: 14px; letter-spacing: 8px; color: #A020F0; text-align: center; margin-bottom: 30px; }}
        div[data-testid="stTextInput"] div[data-baseweb="input"] {{ background: rgba(255, 255, 255, 0.03) !important; backdrop-filter: blur(60px) brightness(0.7) !important; border: 1px solid rgba(160, 32, 240, 0.2) !important; border-radius: 22px !important; position: relative; }}
        div[data-testid="stTextInput"] div[data-baseweb="input"]::after {{ content: "?"; position: absolute; right: 20px; top: 50%; transform: translateY(-50%); color: #A020F0; font-weight: 700; }}
        </style>
    """, unsafe_allow_html=True)

    # Навигация и Плеер (остальной твой код...)
    n1, _, n2 = st.columns([0.15, 0.7, 0.15])
    with n1:
        if st.button("←" if st.session_state.page != "main" else "☰"):
            st.session_state.page = "main" if st.session_state.page != "main" else "library"; st.rerun()
    with n2:
        if st.button("?"): st.session_state.page = "search"; st.rerun()

    if tracks:
        # Здесь логика отображения треков, поиска и кнопок (❮ ▶ ❯ ♥)
        # Код плеера остается таким же, каким он тебе нравился
        st.write(f"<div style='text-align:center; opacity:0.5;'>playing as {st.session_state.user_name}</div>", unsafe_allow_html=True)
        # ... (весь блок с кнопками управления треками)
        st.audio(os.path.join(MUSIC_DIR, tracks[st.session_state.track_index]), autoplay=st.session_state.playing)
