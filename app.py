import streamlit as st
import os

# Настройка страницы в стиле Apple (Dark Mode)
st.set_page_config(page_title="Liquid Glass Player", layout="centered")

# CSS для эффекта Liquid Glass и минимализма
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* Контейнер плеера */
    .main-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 40px;
        padding: 60px 20px;
        text-align: center;
        margin-top: 50px;
    }

    /* Названия */
    .track-title { font-size: 28px; font-weight: 700; font-family: -apple-system; margin-bottom: 5px; }
    .track-author { font-size: 18px; opacity: 0.5; font-family: -apple-system; margin-bottom: 40px; }

    /* Стеклянные кнопки Streamlit */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        color: white !important;
        width: 100%;
        height: 60px;
        transition: 0.4s;
    }
    div.stButton > button:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

# Работа с файлами треков
MUSIC_DIR = "music"
if not os.path.exists(MUSIC_DIR):
    os.makedirs(MUSIC_DIR)

tracks = [f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")]

if not tracks:
    st.info("Добавьте mp3 файлы в папку 'music' на GitHub")
else:
    # Индекс текущего трека в сессии
    if 'track_index' not in st.session_state:
        st.session_state.track_index = 0

    current_file = tracks[st.session_state.track_index]
    
    # Парсим имя файла (ожидаем "Автор - Название.mp3")
    display_name = current_file.replace(".mp3", "")
    if " - " in display_name:
        author, title = display_name.split(" - ", 1)
    else:
        author, title = "Unknown Artist", display_name

    # Интерфейс
    st.markdown(f'<div class="main-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="track-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="track-author">{author}</div>', unsafe_allow_html=True)

    # Ряд кнопок: < Включить > Лайк
    cols = st.columns([1, 1, 1, 1, 1])
    
    with cols[1]:
        if st.button("❮"):
            st.session_state.track_index = (st.session_state.track_index - 1) % len(tracks)
            st.rerun()

    with cols[2]:
        play = st.button("▶ / Ⅱ") # Просто визуальная кнопка

    with cols[3]:
        if st.button("❯"):
            st.session_state.track_index = (st.session_state.track_index + 1) % len(tracks)
            st.rerun()
            
    with cols[4]:
        if st.button("♥"):
            st.toast(f"Добавлено в любимое: {title}")

    st.markdown('</div>', unsafe_allow_html=True)

    # Сам аудиоплеер (скрытый или минималистичный под кнопками)
    audio_file = open(os.path.join(MUSIC_DIR, current_file), 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3')

