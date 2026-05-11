import streamlit as st
import os
import random
import base64
from components.auth import registration_screen

# Настройки
st.set_page_config(page_title="cotakbass music", layout="wide", initial_sidebar_state="collapsed")

MUSIC_DIR, BG_DIR = "music", "bg"
for d in [MUSIC_DIR, BG_DIR]:
    if not os.path.exists(d): os.makedirs(d)

tracks = sorted([f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")])
bg_gifs = [f for f in os.listdir(BG_DIR) if f.endswith(".gif")]

# Session State
if 'page' not in st.session_state: st.session_state.page = "main"
if 'user_name' not in st.session_state: st.session_state.user_name = "guest"
if 'auth' not in st.session_state: st.session_state.auth = False
if 'track_index' not in st.session_state: st.session_state.track_index = 0
if 'favorites' not in st.session_state: st.session_state.favorites = set()
if 'playing' not in st.session_state: st.session_state.playing = False
if 'current_bg' not in st.session_state: st.session_state.current_bg = None

# ЛОГИКА ФОНА
bg_html = "background-color: #000000;"
if st.session_state.playing and bg_gifs:
    if st.session_state.current_bg is None:
        st.session_state.current_bg = random.choice(bg_gifs)
    try:
        with open(os.path.join(BG_DIR, st.session_state.current_bg), "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        bg_html = f'background-image: url("data:image/gif;base64,{encoded}"); background-size: cover; background-position: center;'
    except: pass

# --- ЭКРАНЫ ---

if st.session_state.page == "registration":
    registration_screen()
else:
    # ТВОЙ ПЛЕЕР
    st.markdown(f"""
        <style>
        header, footer, #MainMenu, [data-testid="stInputInstructions"], .st-emotion-cache-1pxm666 {{ display: none !important; }}
        .stApp {{ {bg_html} transition: background 0.8s ease; }}
        .stApp::before {{ content: ""; position: absolute; inset: 0; background: rgba(0, 0, 0, 0.85); z-index: -1; }}
        audio {{ display: none !important; }}
        div.stButton > button {{ background: rgba(255, 255, 255, 0.02) !important; backdrop-filter: blur(30px) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 50% !important; color: #A020F0 !important; width: 52px !important; height: 52px !important; transition: 0.3s ease; }}
        .track-info {{ font-size: 16px; font-weight: 300; padding: 18px 0; border-bottom: 1px solid rgba(255,255,255,0.02); color: white; }}
        .app-header {{ font-size: 10px; letter-spacing: 5px; text-transform: lowercase; color: #A020F0; text-align: center; margin-bottom: 45px; opacity: 0.5; }}
        </style>
    """, unsafe_allow_html=True)

    # Навигация (☰ | Плеер | 👤 ?)
    n1, _, n2, n3 = st.columns([0.15, 0.6, 0.12, 0.13])
    with n1:
        if st.button("☰"):
            st.session_state.page = "library" if st.session_state.page != "library" else "main"; st.rerun()
    with n2:
        if st.button("👤"): # Кнопка Профиля / Регистрации
            st.session_state.page = "registration"; st.rerun()
    with n3:
        if st.button("?"):
            st.session_state.page = "search"; st.rerun()

    if tracks:
        if st.session_state.page == "search":
            q = st.text_input("", placeholder="напиши хуйню", key="s_q")
            if q:
                for t in [x for x in tracks if q.lower() in x.lower()]:
                    c1, c2 = st.columns([0.85, 0.15])
                    with c1: st.markdown(f"<div class='track-info'>{t.replace('.mp3', '')}</div>", unsafe_allow_html=True)
                    with c2:
                        if st.button("▶", key=f"s_{t}"):
                            st.session_state.track_index, st.session_state.page, st.session_state.playing = tracks.index(t), "main", True; st.rerun()
        elif st.session_state.page == "library":
            for fav in list(st.session_state.favorites):
                c1, c2 = st.columns([0.85, 0.15])
                with c1: st.markdown(f"<div class='track-info'>{fav.replace('.mp3', '')}</div>", unsafe_allow_html=True)
                with c2:
                    if st.button("▶", key=f"f_{fav}"):
                        st.session_state.track_index, st.session_state.page, st.session_state.playing = tracks.index(fav), "main", True; st.rerun()
        else:
            # Главный экран
            st.markdown('<div class="app-header">cotakbass music</div>', unsafe_allow_html=True)
            curr = tracks[st.session_state.track_index]
            name_c = curr.replace(".mp3", "").replace("_", " ")
            auth, title = name_c.split(", ", 1) if ", " in name_c else ("unknown", name_c)
            st.markdown(f'<div style="text-align:center; margin-top:10vh;"><div style="font-size:42px; font-weight:700; color:white;">{title}</div><div style="color:#A020F0; font-size:18px; margin-bottom:50px;">{auth}</div></div>', unsafe_allow_html=True)
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
            st.audio(os.path.join(MUSIC_DIR, curr), autoplay=st.session_state.playing)
