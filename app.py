import streamlit as st
import os

st.set_page_config(page_title="Glass Music", layout="centered")

# Кастомный CSS для Ultra Glass Apple Style
st.markdown("""
    <style>
    /* Подключаем шрифты Apple */
    html, body, [class*="st-"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }

    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* Основной контейнер без лишних блоков сверху */
    .main-container {
        padding-top: 20px;
        text-align: center;
    }

    /* Название трека и автора */
    .track-title { 
        font-size: 32px; 
        font-weight: 700; 
        letter-spacing: -0.5px;
        margin-bottom: 5px; 
    }
    .track-author { 
        font-size: 18px; 
        opacity: 0.5; 
        font-weight: 400;
        margin-bottom: 40px; 
    }

    /* Ультра-стеклянные кнопки */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(30px) brightness(1.2) !important;
        -webkit-backdrop-filter: blur(30px) brightness(1.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 18px !important;
        color: white !important;
        font-weight: 500 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 55px !important;
        width: 100% !important;
    }
    
    div.stButton > button:hover {
        background: rgba(255, 255, 255, 0.12) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-2px);
    }

    /* Список любимых треков (стеклянная плашка) */
    .favorites-list {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 15px;
        margin-top: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# Логика треков
MUSIC_DIR = "music"
if not os.path.exists(MUSIC_DIR): os.makedirs(MUSIC_DIR)
tracks = sorted([f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")])

if not tracks:
    st.info("Загрузи mp3 в папку music/")
else:
    if 'track_index' not in st.session_state: st.session_state.track_index = 0
    if 'favorites' not in st.session_state: st.session_state.favorites = []

    current_file = tracks[st.session_state.track_index]
    display_name = current_file.replace(".mp3", "")
    author, title = display_name.split(" - ", 1) if " - " in display_name else ("Неизвестен", display_name)

    # Интерфейс
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="track-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="track-author">{author}</div>', unsafe_allow_html=True)

    # Кнопки управления
    c1, c2, c3, c4 = st.columns(4)
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
                st.toast("Добавлено в любимые")

    # Секция "Мои треки"
    st.write("---")
    with st.expander("📂 Мои любимые треки"):
        if not st.session_state.favorites:
            st.write("Тут пока пусто")
        for fav in st.session_state.favorites:
            st.markdown(f"✨ {fav.replace('.mp3', '')}")

    # Скрытый аудио-модуль
    st.audio(os.path.join(MUSIC_DIR, current_file))
