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

# Session State
if 'page' not in st.session_state: st.session_state.page = "main"
if 'track_index' not in st.session_state: st.session_state.track_index = 0
if 'favorites' not in st.session_state: st.session_state.favorites = set()
if 'playing' not in st.session_state: st.session_state.playing = False
if 'current_bg' not in st.session_state: st.session_state.current_bg = None

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

# УЛЬТРА-МИНМАЛИЗМ И ФИКС ПОИСКА
st.markdown(f"""
    <style>
    /* 1. ЖЕСТКОЕ УДАЛЕНИЕ "Press Enter to apply" */
    [data-testid="stInputInstructions"] {{
        display: none !important;
    }}
    .st-emotion-cache-1pxm666 {{
        display: none !important;
    }}
    
    /* Скрываем стандартную надпись внутри инпута */
    input::placeholder {{
        color: rgba(255, 255, 255, 0.3) !important;
    }}

    header, footer, .stDeployButton, #MainMenu {{
        display: none !important;
    }}
    
    html, body, [class*="st-"] {{ font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important; }}
    
    .stApp {{ {bg_html} transition: background 0.8s ease; }}
    .stApp::before {{ content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.9); z-index: -1; }}
    audio {{ display: none !important; }}
    
    /* Стеклянные кнопки навигации (Верхние) */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(40px) !important;
        -webkit-backdrop-filter: blur(40px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 50% !important;
        color: white !important;
        width: 55px !important; height: 55px !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        transition: 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}

    /* ПОЛОСА ПОИСКА - МАТОВОЕ СТЕКЛО */
    div[data-testid="stTextInput"] div[data-baseweb="input"] {{
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(50px) brightness(0.6) !important;
        -webkit-backdrop-filter: blur(50px) brightness(0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 20px !important;
        padding: 5px !important;
    }}
    
    div[data-testid="stTextInput"] input {{
        color: white !important;
        font-size: 18px !important;
        background: transparent !important;
    }}

    /* Список треков */
    .track-info {{ font-size: 16px; font-weight: 300; padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.02); color: white; }}
    .app-header {{ font-size: 9px; letter-spacing: 6px; text-transform: lowercase; color: #A020F0; text-align: center; margin-bottom: 50px; opacity: 0.5; }}
    </style>
    """, unsafe_allow_html=True)

# Навигация: Кнопки разнесены по краям
n1, _, n2 = st.columns([0.15, 0.7, 0.15])
with n1:
    if st.button("←" if st.session_state.page != "main" else "☰"):
        st.session_state.page = "main" if st.session_state.page != "main" else "library"
        st.rerun()
with n2:
    # Иконка поиска теперь ВИДНА
    if st.button("🔍"): 
        st.session_state.page = "search"
        st.rerun()

if not tracks:
    st.info("No tracks")
else:
    if st.session_state.page == "search":
        st.markdown('<div class="app-header">search</div>', unsafe_allow_html=True)
        
        # Инпут теперь чистый
        query = st.text_input("", placeholder="напиши хуйню", key="search_input", label_visibility="collapsed")
        
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

    elif st.session_state.page == "library":
        st.markdown('<div class="app-header">favorites</div>', unsafe_allow_html=True)
        if not st.session_state.favorites:
            st.write("<p style='text-align:center; opacity:0.3;'>медиатека пуста</p>", unsafe_allow_html=True)
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

    else:
        # ГЛАВНЫЙ ЭКРАН
        current_file = tracks[st.session_state.track_index]
        st.markdown('<div class="app-header">cotakbass music</div>', unsafe_allow_html=True)
        name_clean = current_file.replace(".mp3", "").replace("_", " ")
        author, title = name_clean.split(", ", 1) if ", " in name_clean else ("unknown", name_clean)
        
        st.markdown(f'<div style="text-align:center; margin-top:10vh;">', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:44px; font-weight:800; margin-bottom:5px; letter-spacing:-1.5px; color: white;">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:18px; color:#A020F0; margin-bottom:75px; font-weight:300; opacity:0.8;">{author}</div>', unsafe_allow_html=True)
        
        # Кнопки управления
        _, c1, c2, c3, c4, _ = st.columns(6)
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
