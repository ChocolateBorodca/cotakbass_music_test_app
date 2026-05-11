import streamlit as st
import os

st.set_page_config(page_title="Neon Black Player", layout="wide")

# Ультра-черный дизайн
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* Чистая библиотека без наложений */
    .lib-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        max-width: 500px;
        margin: 0 auto;
    }

    /* Стеклянная карточка */
    .glass-card {
        background: rgba(255, 255, 255, 0.01);
        border: 1px solid rgba(160, 32, 240, 0.2);
        border-radius: 40px;
        padding: 50px 30px;
        margin: 50px auto;
        max-width: 550px;
        text-align: center;
    }

    /* Кнопки управления */
    div.stButton > button {
        background: #000000 !important;
        border: 1px solid rgba(160, 32, 240, 0.3) !important;
        border-radius: 50% !important;
        color: #FFFFFF !important;
        width: 65px !important;
        height: 65px !important;
        font-size: 20px !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #A020F0 !important;
        box-shadow: 0 0 15px rgba(160, 32, 240, 0.4);
    }

    /* Тексты */
    .track-title { font-size: 36px; font-weight: 700; margin-bottom: 0px; letter-spacing: -1px; }
    .track-author { font-size: 18px; color: #A020F0; opacity: 0.7; margin-bottom: 40px; }
    
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Инициализация
MUSIC_DIR = "music"
if not os.path.exists(MUSIC_DIR): os.makedirs(MUSIC_DIR)
tracks = sorted([f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")])

if 'page' not in st.session_state: st.session_state.page = "main"
if 'track_index' not in st.session_state: st.session_state.track_index = 0
if 'favorites' not in st.session_state: st.session_state.favorites = set() # Используем set для уникальности
if 'playing' not in st.session_state: st.session_state.playing = False

# Навигация (Кнопка меню)
c_nav, _ = st.columns([0.1, 0.9])
with c_nav:
    if st.button("☰" if st.session_state.page == "main" else "←"):
        st.session_state.page = "library" if st.session_state.page == "main" else "main"
        st.rerun()

if not tracks:
    st.info("Добавь музыку в папку music/")
else:
    current_file = tracks[st.session_state.track_index]

    if st.session_state.page == "library":
        st.markdown('<h1 style="text-align:center;">Избранное</h1>', unsafe_allow_html=True)
        if not st.session_state.favorites:
            st.write("<p style='text-align:center;'>Тут пока пусто</p>", unsafe_allow_html=True)
        else:
            for fav in list(st.session_state.favorites):
                # Каждая кнопка трека в библиотеке теперь на всю ширину и аккуратная
                if st.button(f"🎵 {fav.replace('.mp3', '')}", key=fav, use_container_width=True):
                    st.session_state.track_index = tracks.index(fav)
                    st.session_state.page = "main"
                    st.session_state.playing = True
                    st.rerun()

    else:
        # Основной интерфейс плеера
        display_name = current_file.replace(".mp3", "")
        author, title = display_name.split(" - ", 1) if " - " in display_name else ("Unknown", display_name)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="track-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="track-author">{author}</div>', unsafe_allow_html=True)
        
        # Кнопки в один ряд: Назад - Вкл/Выкл - Вперед - Лайк
        c1, c2, c3, c4, c5, c6 = st.columns([1,1,1,1,1,1])
        with c2:
            if st.button("❮"):
                st.session_state.track_index = (st.session_state.track_index - 1) % len(tracks)
                st.rerun()
        with c3:
            play_icon = "Ⅱ" if st.session_state.playing else "▶"
            if st.button(play_icon):
                st.session_state.playing = not st.session_state.playing
                st.rerun()
        with c4:
            if st.button("❯"):
                st.session_state.track_index = (st.session_state.track_index + 1) % len(tracks)
                st.rerun()
        with c5:
            is_fav = current_file in st.session_state.favorites
            if st.button("💜" if is_fav else "🤍"):
                if is_fav: st.session_state.favorites.remove(current_file)
                else: st.session_state.favorites.add(current_file)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Логика самого плеера
    audio_path = os.path.join(MUSIC_DIR, current_file)
    if st.session_state.playing:
        st.audio(audio_path, autoplay=True)
    else:
        st.audio(audio_path, autoplay=False)
