import streamlit as st
import os
import random

st.set_page_config(page_title="cotakbass music", layout="wide")

# Логика работы с файлами
MUSIC_DIR = "music"
BG_DIR = "bg" # Папка для твоих GIF

for d in [MUSIC_DIR, BG_DIR]:
    if not os.path.exists(d): os.makedirs(d)

tracks = sorted([f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")])
bg_gifs = [f for f in os.listdir(BG_DIR) if f.endswith(".gif")]

# Инициализация сессии
if 'page' not in st.session_state: st.session_state.page = "main"
if 'track_index' not in st.session_state: st.session_state.track_index = 0
if 'favorites' not in st.session_state: st.session_state.favorites = set()
if 'playing' not in st.session_state: st.session_state.playing = False
if 'current_bg' not in st.session_state: st.session_state.current_bg = None

# Выбор случайного фона при смене трека или включении
if st.session_state.playing and bg_gifs:
    if st.session_state.current_bg is None:
        st.session_state.current_bg = random.choice(bg_gifs)
else:
    st.session_state.current_bg = None

# Кастомный CSS с поддержкой GIF-фона
bg_style = ""
if st.session_state.current_bg:
    bg_url = f"bg/{st.session_state.current_bg}"
    # Используем хак для отображения локального файла как фона
    import base64
    with open(os.path.join(BG_DIR, st.session_state.current_bg), "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
    bg_style = f"""
        background-image: url("data:image/gif;base64,{encoded}");
        background-size: cover;
        background-position: center;
    """

st.markdown(f"""
    <style>
    html, body, [class*="st-"] {{
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important;
    }}
    .stApp {{
        {bg_style if st.session_state.playing else "background-color: #000000;"}
        transition: background 1s ease-in-out;
    }}
    
    /* Затемнение фона для читаемости */
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.6);
        z-index: -1;
    }}

    audio {{ display: none !important; }}

    .app-header {{
        font-size: 16px; font-weight: 500; letter-spacing: 3px;
        text-transform: lowercase; color: #A020F0;
        margin-bottom: 50px; text-align: center;
    }}

    /* Стеклянные кнопки с анимацией */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(160, 32, 240, 0.3) !important;
        border-radius: 50px !important;
        color: white !important;
        transition: all 0.4s ease !important;
    }}
    div.stButton > button:hover {{
        transform: translateY(-5px) scale(1.1) !important;
        box-shadow: 0 10px 20px rgba(160, 32, 240, 0.3);
    }}

    header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# Кнопка навигации
nav_c, _ = st.columns([0.1, 0.9])
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
        for fav in list(st.session_state.favorites):
            col_name, col_btn = st.columns([0.85, 0.15])
            with col_name:
                st.markdown(f"<div style='padding-top:10px; border-bottom: 1px solid rgba(255,255,255,0.1)'>{fav.replace('.mp3', '')}</div>", unsafe_allow_html=True)
            with col_btn:
                if st.button("▶", key=f"play_{fav}"):
                    st.session_state.track_index = tracks.index(fav)
                    st.session_state.page = "main"
                    st.session_state.playing = True
                    st.session_state.current_bg = None # Сброс фона для нового выбора
                    st.rerun()
    else:
        # Главный экран
        st.markdown('<div class="app-header">cotakbass music</div>', unsafe_allow_html=True)
        display_name = current_file.replace(".mp3", "").replace("_", " ")
        author, title = display_name.split(", ", 1) if ", " in display_name else ("unknown artist", display_name)
        
        st.markdown(f'<div style="text-align:center; margin-top:5vh;">', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:42px; font-weight:700; margin-bottom:10px; text-shadow: 0 4px 15px rgba(0,0,0,0.5);">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:18px; color:#A020F0; margin-bottom:60px;">{author}</div>', unsafe_allow_html=True)
        
        _, c1, c2, c3, c4, _ = st.columns()
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

    st.audio(os.path.join(MUSIC_DIR, current_file), autoplay=st.session_state.playing)
