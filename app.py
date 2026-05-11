import streamlit as st
import os

st.set_page_config(page_title="COTKBASS MUSIC", layout="wide")

# Ультра-минималистичный Apple CSS
st.markdown("""
    <style>
    /* Вернули Apple шрифты */
    html, body, [class*="st-"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", sans-serif !important;
    }

    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* Скрываем стандартный аудио-плеер (серую линию) */
    audio { display: none !important; }
    
    /* Название приложения вместо пустого блока */
    .app-header {
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #A020F0;
        margin-bottom: 60px;
        text-align: center;
        opacity: 0.8;
    }

    /* Основная стеклянная панель */
    .player-container {
        text-align: center;
        margin-top: 5vh;
    }

    /* Названия */
    .track-title { 
        font-size: 38px; 
        font-weight: 700; 
        letter-spacing: -1px; 
        margin-bottom: 8px; 
        color: white;
    }
    .track-author { 
        font-size: 18px; 
        color: #A020F0; 
        font-weight: 400; 
        margin-bottom: 50px; 
    }

    /* Ультра-стеклянные кнопки */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(160, 32, 240, 0.2) !important;
        border-radius: 50% !important;
        color: white !important;
        width: 70px !important;
        height: 70px !important;
        transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    div.stButton > button:hover {
        border-color: #A020F0 !important;
        background: rgba(160, 32, 240, 0.1) !important;
        transform: scale(1.1);
    }

    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Инициализация
MUSIC_DIR = "music"
if not os.path.exists(MUSIC_DIR): os.makedirs(MUSIC_DIR)
tracks = sorted([f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")])

if 'page' not in st.session_state: st.session_state.page = "main"
if 'track_index' not in st.session_state: st.session_state.track_index = 0
if 'favorites' not in st.session_state: st.session_state.favorites = set()
if 'playing' not in st.session_state: st.session_state.playing = False

# Навигация (Кнопка меню в углу)
nav_col, _ = st.columns([0.1, 0.9])
with nav_col:
    if st.button("☰" if st.session_state.page == "main" else "←"):
        st.session_state.page = "library" if st.session_state.page == "main" else "main"
        st.rerun()

if not tracks:
    st.info("Добавь музыку в /music")
else:
    current_file = tracks[st.session_state.track_index]

    if st.session_state.page == "library":
        st.markdown('<div class="app-header">Favorites</div>', unsafe_allow_html=True)
        if not st.session_state.favorites:
            st.write("<p style='text-align:center; opacity:0.5;'>Тут пусто</p>", unsafe_allow_html=True)
        else:
            for fav in list(st.session_state.favorites):
                if st.button(f" {fav.replace('.mp3', '')}", key=fav, use_container_width=True):
                    st.session_state.track_index = tracks.index(fav)
                    st.session_state.page = "main"
                    st.session_state.playing = True
                    st.rerun()

    else:
        # Плеер
        st.markdown('<div class="app-header">COTKBASS MUSIC</div>', unsafe_allow_html=True)
        
        display_name = current_file.replace(".mp3", "").replace("_", " ")
        author, title = display_name.split(", ", 1) if ", " in display_name else ("Unknown Artist", display_name)
        
        st.markdown('<div class="player-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="track-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="track-author">{author}</div>', unsafe_allow_html=True)
        
        # Кнопки управления (ровно по центру)
        _, c1, c2, c3, c4, _ = st.columns([1, 1, 1, 1, 1, 1])
        with c1:
            if st.button("❮"):
                st.session_state.track_index = (st.session_state.track_index - 1) % len(tracks)
                st.rerun()
        with c2:
            icon = "Ⅱ" if st.session_state.playing else "▶"
            if st.button(icon):
                st.session_state.playing = not st.session_state.playing
                st.rerun()
        with c3:
            if st.button("❯"):
                st.session_state.track_index = (st.session_state.track_index + 1) % len(tracks)
                st.rerun()
        with c4:
            is_fav = current_file in st.session_state.favorites
            if st.button("💜" if is_fav else "🤍"):
                if is_fav: st.session_state.favorites.remove(current_file)
                else: st.session_state.favorites.add(current_file)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Сам аудио-движок (теперь скрыт)
    audio_path = os.path.join(MUSIC_DIR, current_file)
    st.audio(audio_path, autoplay=st.session_state.playing)
