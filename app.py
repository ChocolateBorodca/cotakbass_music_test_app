import streamlit as st
import os
import random
import base64
from components.auth import registration_screen

# ТВОЙ КОД: Настройки
st.set_page_config(page_title="cotakbass music", layout="wide", initial_sidebar_state="collapsed")

# Настройки папок
MUSIC_DIR = "music"
BG_DIR = "bg"
for d in [MUSIC_DIR, BG_DIR]:
    if not os.path.exists(d): os.makedirs(d)

tracks = sorted([f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")])
bg_gifs = [f for f in os.listdir(BG_DIR) if f.endswith(".gif")]

# ТВОЙ КОД: Session State
if 'page' not in st.session_state: st.session_state.page = "main"
if 'track_index' not in st.session_state: st.session_state.track_index = 0
if 'favorites' not in st.session_state: st.session_state.favorites = set()
if 'playing' not in st.session_state: st.session_state.playing = False
if 'current_bg' not in st.session_state: st.session_state.current_bg = None
if 'auth' not in st.session_state: st.session_state.auth = False

# --- ЛОГИКА ЗАПУСКА ---
if not st.session_state.auth:
    registration_screen()
else:
    # --- ВЕСЬ ТВОЙ КОД ПЛЕЕРА ---
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

    st.markdown(f"""
        <style>
        [data-testid="stInputInstructions"], .st-emotion-cache-1pxm666, [data-baseweb="helper-text"] {{
            display: none !important; height: 0px !important;
        }}
        header, footer, .stDeployButton, #MainMenu {{ display: none !important; }}
        html, body, [class*="st-"] {{ font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important; }}
        .stApp {{ {bg_html} transition: background 0.8s ease; }}
        .stApp::before {{ content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.93); z-index: -1; }}
        audio {{ display: none !important; }}
        
        div.stButton > button {{
            background: rgba(255, 255, 255, 0.02) !important;
            backdrop-filter: blur(40px) !important;
            -webkit-backdrop-filter: blur(40px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 50% !important;
            color: #A020F0 !important;
            width: 52px !important; height: 52px !important;
            display: flex !important; align-items: center !important; justify-content: center !important;
            transition: 0.35s ease !important;
            font-weight: 600 !important;
        }}

        .search-title-photo {{ font-size: 14px; letter-spacing: 8px; color: #A020F0; text-align: center; margin-bottom: 30px; }}
        div[data-testid="stTextInput"] div[data-baseweb="input"] {{ background: rgba(255, 255, 255, 0.03) !important; backdrop-filter: blur(60px) brightness(0.7) !important; border: 1px solid rgba(160, 32, 240, 0.2) !important; border-radius: 22px !important; position: relative; }}
        div[data-testid="stTextInput"] div[data-baseweb="input"]::after {{ content: "?"; position: absolute; right: 20px; top: 50%; transform: translateY(-50%); color: #A020F0; font-weight: 700; font-size: 18px; }}
        div[data-testid="stTextInput"] input {{ color: white !important; background: transparent !important; padding: 20px 50px 20px 20px !important; border: none !important; }}
        div[data-testid="stTextInput"] label {{ display: none !important; }}
        .track-info {{ font-size: 16px; font-weight: 300; padding: 18px 0; border-bottom: 1px solid rgba(255,255,255,0.02); color: white; }}
        .app-header {{ font-size: 10px; letter-spacing: 5px; text-transform: lowercase; color: #A020F0; text-align: center; margin-bottom: 45px; opacity: 0.5; }}
        </style>
    """, unsafe_allow_html=True)

    # Навигация (из Файла 2)
    n1, _, n2 = st.columns([0.15, 0.7, 0.15])
    with n1:
        if st.button("←" if st.session_state.page != "main" else "☰"):
            st.session_state.page = "main" if st.session_state.page != "main" else "library"; st.rerun()
    with n2:
        if st.button("?"): st.session_state.page = "search"; st.rerun()

    if not tracks:
        st.info("No tracks")
    else:
        if st.session_state.page == "search":
            st.markdown('<div class="search-title-photo">search</div>', unsafe_allow_html=True)
            query = st.text_input("", placeholder="напиши хуйню", key="search_input")
            if query:
                for track in [t for t in tracks if query.lower() in t.lower()]:
                    c_n, c_p = st.columns([0.85, 0.15])
                    with c_n: st.markdown(f"<div class='track-info'>{track.replace('.mp3', '')}</div>", unsafe_allow_html=True)
                    with c_p:
                        if st.button("▶", key=f"s_{track}"):
                            st.session_state.track_index, st.session_state.page, st.session_state.playing = tracks.index(track), "main", True; st.rerun()

        elif st.session_state.page == "library":
            st.markdown('<div class="app-header">favorites</div>', unsafe_allow_html=True)
            for fav in list(st.session_state.favorites):
                c_n, c_p = st.columns([0.85, 0.15])
                with c_n: st.markdown(f"<div class='track-info'>{fav.replace('.mp3', '')}</div>", unsafe_allow_html=True)
                with c_p:
                    if st.button("▶", key=f"f_{fav}"):
                        st.session_state.track_index, st.session_state.page, st.session_state.playing = tracks.index(fav), "main", True; st.rerun()

        else:
            # ГЛАВНЫЙ ЭКРАН (из Файла 3)
            st.markdown('<div class="app-header">cotakbass music</div>', unsafe_allow_html=True)
            curr = tracks[st.session_state.track_index]
            name_clean = curr.replace(".mp3", "").replace("_", " ")
            author, title = name_clean.split(", ", 1) if ", " in name_clean else ("unknown", name_clean)
            
            st.markdown(f'<div style="text-align:center; margin-top:10vh;"><div style="font-size:42px; font-weight:700; margin-bottom:5px; letter-spacing:-1.5px; color: white;">{title}</div><div style="font-size:18px; color:#A020F0; margin-bottom:65px; font-weight:300;">{author}</div></div>', unsafe_allow_html=True)
            
            _, c1, c2, c3, c4, _ = st.columns(6)
            with c1:
                if st.button("❮"): st.session_state.track_index = (st.session_state.track_index - 1) % len(tracks); st.session_state.current_bg = None; st.rerun()
            with c2:
                if st.button("Ⅱ" if st.session_state.playing else "▶"): st.session_state.playing = not st.session_state.playing; st.rerun()
            with c3:
                if st.button("❯"): st.session_state.track_index = (st.session_state.track_index + 1) % len(tracks); st.session_state.current_bg = None; st.rerun()
            with c4:
                is_fav = curr in st.session_state.favorites
                if st.button("💜" if is_fav else "🤍"):
                    if is_fav: st.session_state.favorites.remove(curr)
                    else: st.session_state.favorites.add(curr); st.snow()
                    st.rerun()
        
        st.audio(os.path.join(MUSIC_DIR, tracks[st.session_state.track_index]), autoplay=st.session_state.playing)
