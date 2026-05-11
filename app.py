import streamlit as st
import os

st.set_page_config(page_title="Glass Music", layout="wide")

# Ультра-стеклянный CSS с навигацией
st.markdown("""
    <style>
    html, body, [class*="st-"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important;
    }
    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* Стеклянная кнопка библиотеки в углу */
    .nav-button-container {
        position: absolute;
        top: 20px;
        left: 20px;
        z-index: 1000;
    }

    /* Ультра-стекло для всех кнопок */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(40px) brightness(1.3) !important;
        -webkit-backdrop-filter: blur(40px) brightness(1.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        color: white !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }

    /* Стили текста */
    .track-title { font-size: 42px; font-weight: 700; margin-bottom: 0px; letter-spacing: -1px; }
    .track-author { font-size: 20px; opacity: 0.4; margin-bottom: 40px; }
    .lib-title { font-size: 32px; font-weight: 700; margin-bottom: 30px; }
    
    /* Убираем стандартные отступы Streamlit */
    .block-container { padding-top: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# Инициализация данных
MUSIC_DIR = "music"
if not os.path.exists(MUSIC_DIR): os.makedirs(MUSIC_DIR)
tracks = sorted([f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")])

if 'page' not in st.session_state: st.session_state.page = "main"
if 'track_index' not in st.session_state: st.session_state.track_index = 0
if 'favorites' not in st.session_state: st.session_state.favorites = []

# КНОПКА В УГЛУ (Слева сверху)
col_nav, _ = st.columns([1, 10])
with col_nav:
    if st.session_state.page == "main":
        if st.button("Favorites"):
            st.session_state.page = "library"
            st.rerun()
    else:
        if st.button("← Back"):
            st.session_state.page = "main"
            st.rerun()

# --- ЛОГИКА ЭКРАНОВ ---

if not tracks:
    st.info("Загрузи музыку в папку music/")
else:
    current_file = tracks[st.session_state.track_index]
    
    # ЭКРАН: БИБЛИОТЕКА
    if st.session_state.page == "library":
        st.markdown('<div class="lib-title">Любимые треки</div>', unsafe_allow_html=True)
        if not st.session_state.favorites:
            st.write("Список пуст. Нажми ♥ на главном экране.")
        else:
            for i, fav in enumerate(st.session_state.favorites):
                # Стеклянная плашка трека
                if st.button(f"🎵 {fav.replace('.mp3', '')}", key=f"fav_{i}"):
                    # Находим индекс этого трека в общем списке, чтобы включить его
                    st.session_state.track_index = tracks.index(fav)
                    st.session_state.page = "main"
                    st.rerun()

    # ЭКРАН: ПЛЕЕР (ГЛАВНЫЙ)
    else:
        display_name = current_file.replace(".mp3", "")
        author, title = display_name.split(" - ", 1) if " - " in display_name else ("Unknown", display_name)
        
        st.markdown(f'<div style="text-align: center; margin-top: 10vh;">', unsafe_allow_html=True)
        st.markdown(f'<div class="track-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="track-author">{author}</div>', unsafe_allow_html=True)
        
        # Кнопки управления
        _, c1, c2, c3, c4, _ = st.columns([1, 1, 1, 1, 1, 1])
        with c1:
            if st.button("❮"):
                st.session_state.track_index = (st.session_state.track_index - 1) % len(tracks)
                st.rerun()
        with c2:
            st.button("▶ / Ⅱ")
        with c3:
            if st.button("❯"):
                st.session_state.track_index = (st.session_state.track_index + 1) % len(tracks)
                st.rerun()
        with c4:
            if st.button("♥"):
                if current_file not in st.session_state.favorites:
                    st.session_state.favorites.append(current_file)
                    st.toast("Добавлено в медиатеку")
        st.markdown('</div>', unsafe_allow_html=True)

    # ОБЩИЙ ПЛЕЕР (Всегда внизу)
    st.write("")
    st.audio(os.path.join(MUSIC_DIR, current_file))
