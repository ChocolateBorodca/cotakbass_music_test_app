import streamlit as st
import os

st.set_page_config(page_title="cotakbass music", layout="wide")

# Ультра-минимализм и анимации
st.markdown("""
    <style>
    /* Шрифт Apple */
    html, body, [class*="st-"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important;
    }
    .stApp { background-color: #000000; color: #FFFFFF; }
    audio { display: none !important; }

    /* Название приложения */
    .app-header {
        font-size: 16px;
        font-weight: 500;
        letter-spacing: 3px;
        text-transform: lowercase;
        color: #A020F0;
        margin-bottom: 50px;
        text-align: center;
        opacity: 0.9;
    }

    /* Анимация всплытия кнопок */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(160, 32, 240, 0.2) !important;
        border-radius: 50px !important;
        color: white !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-5px) scale(1.1) !important;
        border-color: #A020F0 !important;
        box-shadow: 0 10px 20px rgba(160, 32, 240, 0.2);
    }

    /* Горизонтальный трек в библиотеке */
    .lib-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 25px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 20px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.05);
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
                col_name, col_btn = st.columns([0.85, 0.15])
                with col_name:
                    st.markdown(f"<div style='padding-top:10px;'>{fav.replace('.mp3', '')}</div>", unsafe_allow_html=True)
                with col_btn:
                    if st.button("▶", key=f"play_{fav}"):
                        st.session_state.track_index = tracks.index(fav)
                        st.session_state.page = "main"
                        st.session_state.playing = True
                        st.rerun()

    else:
        # Главный экран
        st.markdown('<div class="app-header">cotakbass music</div>', unsafe_allow_html=True)
        
        display_name = current_file.replace(".mp3", "").replace("_", " ")
        author, title = display_name.split(", ", 1) if ", " in display_name else ("unknown artist", display_name)
        
        st.markdown(f'<div style="text-align:center; margin-top:5vh;">', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:42px; font-weight:700; margin-bottom:10px;">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:18px; color:#A020F0; margin-bottom:60px;">{author}</div>', unsafe_allow_html=True)
        
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
                if is_fav:
                    st.session_state.favorites.remove(current_file)
                else:
                    st.session_state.favorites.add(current_file)
                    st.snow() # Эффект "вылетающих" снежинок/частиц как аналог сердечек
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Аудио движок
    st.audio(os.path.join(MUSIC_DIR, current_file), autoplay=st.session_state.playing)
