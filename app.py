import streamlit as st
import os
import random
import base64

# Установка названия вкладки и иконки
st.set_page_config(page_title="cotakbass music", layout="wide", initial_sidebar_state="collapsed")

# Настройки папок
MUSIC_DIR = "music"
BG_DIR = "bg"

for d in [MUSIC_DIR, BG_DIR]:
    if not os.path.exists(d): 
        os.makedirs(d)

# Получаем списки файлов
tracks = sorted([f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")])
bg_gifs = [f for f in os.listdir(BG_DIR) if f.endswith(".gif")]

# Инициализация состояния (Session State)
if 'page' not in st.session_state: st.session_state.page = "main"
if 'track_index' not in st.session_state: st.session_state.track_index = 0
if 'favorites' not in st.session_state: st.session_state.favorites = set()
if 'playing' not in st.session_state: st.session_state.playing = False
if 'current_bg' not in st.session_state: st.session_state.current_bg = None

# Логика выбора случайного GIF-фона
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

# Ультра-минимализм Apple + Анимации
st.markdown(f"""
    <style>
    html, body, [class*="st-"] {{
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important;
    }}
    .stApp {{
        {bg_style}
        transition: background 1s ease-in-out;
    }}
    /* Затемнение для читаемости */
    .stApp::before {{
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.7); z-index: -1;
    }}
    audio {{ display: none !important; }}
    .app-header {{
        font-size: 14px; font-weight: 500; letter-spacing: 4px;
        text-transform: lowercase; color: #A020F0;
        margin-bottom: 40px; text-align: center; opacity: 0.8;
    }}
    /* Кнопки с эффектом всплытия */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(160, 32, 240, 0.2) !important;
        border-radius: 50% !important;
        color: white !important;
        width: 70px !important; height: 70px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }}
    div.stButton > button:hover {{
        transform: translateY(-8px) scale(1.1) !important;
        border-color: #A020F0 !important;
        box-shadow: 0 15px 30px rgba(160, 32, 240, 0.3);
    }}
    /* Библиотека горизонтально */
    .track-row {{
        padding: 15px; border-bottom: 1px solid rgba(255,255,255,0.05);
        display: flex; justify-content: space-between; align-items: center;
    }}
    header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# Навигация
nav_c, _ = st.columns([0.1, 0.9])
with nav_c:
    if st.button("←" if st.session_state.page == "library" else "☰"):
        st.session_state.page = "library" if st.session_state.page == "main" else "main"
        st.rerun()

if not tracks:
    st.info("Добавь музыку в папку music/")
else:
    current_file = tracks[st.session_state.track_index]

    if st.session_state.page == "library":
        st.markdown('<div class="app-header">favorites</div>', unsafe_allow_html=True)
        if not st.session_state.favorites:
            st.write("<p style='text-align:center; opacity:0.5;'>Пусто</p>", unsafe_allow_html=True)
        else:
            for fav in list(st.session_state.favorites):
                col_t, col_b = st.columns([0.8, 0.2])
                with col_t: st.markdown(f"<div style='padding-top:20px; font-size:18px;'>{fav.replace('.mp3', '').replace('_', ' ')}</div>", unsafe_allow_html=True)
                with col_b:
                    if st.button("▶", key=f"fav_play_{fav}"):
                        st.session_state.track_index = tracks.index(fav)
                        st.session_state.page = "main"
                        st.session_state.playing = True
                        st.rerun()

    else:
        # Главный экран
        st.markdown('<div class="app-header">cotakbass music</div>', unsafe_allow_html=True)
        
        name_clean = current_file.replace(".mp3", "").replace("_", " ")
        author, title = name_clean.split(", ", 1) if ", " in name_clean else ("unknown", name_clean)
        
        st.markdown(f'<div style="text-align:center; margin-top:5vh;">', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:48px; font-weight:700; letter-spacing:-1px;">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:20px; color:#A020F0; margin-bottom:60px; opacity:0.8;">{author}</div>', unsafe_allow_html=True)
        
        # Кнопки (исправлено количество колонок на 6)
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

    # Аудио движок
    st.audio(os.path.join(MUSIC_DIR, current_file), autoplay=st.session_state.playing)
