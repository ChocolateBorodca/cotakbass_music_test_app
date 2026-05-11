import streamlit as st
import os
import random
import base64
from components.auth import registration_screen, profile_screen

# 1. Настройка страницы
st.set_page_config(page_title="cotakbass music", layout="wide", initial_sidebar_state="collapsed")

# Папки
MUSIC_DIR, BG_DIR = "music", "bg"
for d in [MUSIC_DIR, BG_DIR]:
    if not os.path.exists(d): os.makedirs(d)

# 2. Инициализация Session State (ФИКС ОШИБОК)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user' not in st.session_state or not isinstance(st.session_state.user, dict):
    st.session_state.user = {"name": "guest", "bio": "", "ava": None}
if 'page' not in st.session_state: st.session_state.page = "main"
if 'track_index' not in st.session_state: st.session_state.track_index = 0
if 'favorites' not in st.session_state: st.session_state.favorites = set()
if 'playing' not in st.session_state: st.session_state.playing = False
if 'current_bg' not in st.session_state: st.session_state.current_bg = None

# 3. Логика динамического GIF-фона
bg_css = "background-color: #000000;"
bg_gifs = [f for f in os.listdir(BG_DIR) if f.endswith(".gif")]
if st.session_state.playing and bg_gifs:
    if st.session_state.current_bg is None:
        st.session_state.current_bg = random.choice(bg_gifs)
    try:
        with open(os.path.join(BG_DIR, st.session_state.current_bg), "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        bg_css = f'background-image: url("data:image/gif;base64,{encoded}"); background-size: cover; background-position: center;'
    except: pass
else:
    st.session_state.current_bg = None

# 4. УЛЬТРА-МАТОВЫЙ CSS (Стиль Apple + Neon Purple)
online_glow = "box-shadow: 0 0 20px #A020F0; border: 2px solid #A020F0 !important;" if st.session_state.auth else "border: 1px solid rgba(255,255,255,0.1) !important;"

st.markdown(f"""
    <style>
    header, footer, #MainMenu, [data-testid="stInputInstructions"], .st-emotion-cache-oc994i {{ display: none !important; }}
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

    /* Свечение аватарки в навигации */
    .nav-profile-btn button {{ {online_glow} }}

    /* НАЗВАНИЕ ТРЕКА СЛЕВА */
    .track-info-left {{
        text-align: left;
        padding-left: 5%;
        margin-top: 10vh;
    }}
    .title-text {{ font-size: 44px; font-weight: 800; color: white; letter-spacing: -1.5px; line-height: 1; }}
    .author-text {{ font-size: 18px; color: #A020F0; font-weight: 300; margin-top: 5px; margin-bottom: 60px; }}

    /* МАТОВЫЙ ПОИСК С "?" ВНУТРИ */
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
    .app-header {{ font-size: 10px; letter-spacing: 5px; text-transform: lowercase; color: #A020F0; text-align: center; margin-bottom: 45px; opacity: 0.5; }}
    </style>
""", unsafe_allow_html=True)

# 5. ЛОГИКА ЭКРАНОВ
if st.session_state.page == "registration":
    registration_screen()
elif st.session_state.page == "profile":
    profile_screen()
else:
    # --- ГЛАВНЫЙ ЭКРАН ПЛЕЕРА ---
    # Навигация (☰ | 👤 | ?)
    n1, _, n2, n3 = st.columns([0.15, 0.6, 0.12, 0.13])
    with n1:
        if st.button("☰"): st.session_state.page = "library"; st.rerun()
    with n2:
        st.markdown('<div class="nav-profile-btn">', unsafe_allow_html=True)
        if st.button("👤"): 
            st.session_state.page = "profile" if st.session_state.auth else "registration"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with n3:
        if st.button("?"): st.session_state.page = "search"; st.rerun()

    tracks = sorted([f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")])
    
    if not tracks:
        st.info("No tracks in /music")
    else:
        # Экран ПОИСКА
        if st.session_state.page == "search":
            q = st.text_input("", placeholder="напиши хуйню", key="s_q")
            if q:
                for t in [x for x in tracks if q.lower() in x.lower()]:
                    c_t, c_p = st.columns([0.85, 0.15])
                    with c_t: st.markdown(f"<div class='list-item'>{t.replace('.mp3', '')}</div>", unsafe_allow_html=True)
                    with c_p:
                        if st.button("▶", key=f"s_{t}"):
                            st.session_state.track_index, st.session_state.page, st.session_state.playing = tracks.index(t), "main", True; st.rerun()
        
        # Экран МЕДИАТЕКИ
        elif st.session_state.page == "library":
            st.markdown('<div class="app-header">favorites</div>', unsafe_allow_html=True)
            for f in list(st.session_state.favorites):
                c_t, c_p = st.columns([0.85, 0.15])
                with c_t: st.markdown(f"<div class='list-item'>{f.replace('.mp3', '')}</div>", unsafe_allow_html=True)
                with c_p:
                    if st.button("▶", key=f"l_{f}"):
                        st.session_state.track_index, st.session_state.page, st.session_state.playing = tracks.index(f), "main", True; st.rerun()
        
        # ОСНОВНОЙ ПЛЕЕР
        else:
            st.markdown('<div class="app-header">cotakbass music</div>', unsafe_allow_html=True)
            curr = tracks[st.session_state.track_index]
            name_c = curr.replace(".mp3", "").replace("_", " ")
            auth, title = name_c.split(", ", 1) if ", " in name_c else ("unknown", name_c)
            
            st.markdown(f"""
                <div class="track-info-left">
                    <div class="title-text">{title}</div>
                    <div class="author-text">{auth}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Кнопки управления
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
