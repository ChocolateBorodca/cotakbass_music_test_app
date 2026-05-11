import streamlit as st
import os

st.set_page_config(page_title="Neon Glass Player", layout="wide")

# Кастомный CSS: Черный + Фиолетовый Неон
st.markdown("""
    <style>
    /* Глубокий черный фон с виньеткой */
    .stApp {
        background: radial-gradient(circle, #1a0b2e 0%, #000000 100%);
        color: #FFFFFF;
    }

    /* Шрифты Apple */
    html, body, [class*="st-"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important;
    }

    /* Стеклянная карточка с неоновой обводкой */
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border: 1px solid rgba(160, 32, 240, 0.3); /* Фиолетовый неон */
        border-radius: 50px;
        padding: 60px 40px;
        box-shadow: 0 0 30px rgba(160, 32, 240, 0.1);
        margin: auto;
        max-width: 550px;
        text-align: center;
    }

    /* Центрирование кнопок в одну линию */
    [data-testid="stHorizontalBlock"] {
        align-items: center;
        justify-content: center;
    }

    /* Неоновые кнопки-капли */
    div.stButton > button {
        background: rgba(160, 32, 240, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(160, 32, 240, 0.4) !important;
        border-radius: 100px !important;
        color: #e0aaff !important;
        font-size: 20px !important;
        height: 65px !important;
        width: 65px !important;
        transition: all 0.4s ease;
        box-shadow: 0 0 10px rgba(160, 32, 240, 0.2);
    }
    
    div.stButton > button:hover {
        background: rgba(160, 32, 240, 0.2) !important;
        border: 1px solid rgba(160, 32, 240, 0.8) !important;
        box-shadow: 0 0 25px rgba(160, 32, 240, 0.5);
        transform: scale(1.1);
    }

    /* Текст */
    .track-title { 
        font-size: 40px; 
        font-weight: 700; 
        letter-spacing: -1.5px;
        color: #ffffff;
        text-shadow: 0 0 20px rgba(160, 32, 240, 0.4);
        margin-bottom: 5px;
    }
    .track-author { 
        font-size: 20px; 
        color: #a020f0; 
        opacity: 0.8;
        font-weight: 400; 
        margin-bottom: 50px; 
    }
    
    /* Скрываем лишнее */
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

# Логика работы с треками
MUSIC_DIR = "music"
if not os.path.exists(MUSIC_DIR): os.makedirs(MUSIC_DIR)
tracks = sorted([f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")])

if 'page' not in st.session_state: st.session_state.page = "main"
if 'track_index' not in st.session_state: st.session_state.track_index = 0
if 'favorites' not in st.session_state: st.session_state.favorites = []

# Кнопка Библиотеки (Слева сверху)
c_nav, _ = st.columns([1, 5])
with c_nav:
    label = "←" if st.session_state.page == "library" else "☰"
    if st.button(label):
        st.session_state.page = "main" if st.session_state.page == "library" else "library"
        st.rerun()

if not tracks:
    st.info("Добавь музыку в /music")
else:
    current_file = tracks[st.session_state.track_index]

    if st.session_state.page == "library":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="track-title" style="font-size: 28px">Избранное</div>', unsafe_allow_html=True)
        for fav in st.session_state.favorites:
            if st.button(f"🟣 {fav.replace('.mp3', '')}"):
                st.session_state.track_index = tracks.index(fav)
                st.session_state.page = "main"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        # Плеер
        display_name = current_file.replace(".mp3", "")
        author, title = display_name.split(" - ", 1) if " - " in display_name else ("Unknown", display_name)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="track-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="track-author">{author}</div>', unsafe_allow_html=True)
        
        # Ряд кнопок: Назад - Плей - Вперед - Лайк
        c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 1])
        with c2:
            if st.button("❮"):
                st.session_state.track_index = (st.session_state.track_index - 1) % len(tracks)
                st.rerun()
        with c3:
            st.button("▶") # Центральная кнопка
        with c4:
            if st.button("❯"):
                st.session_state.track_index = (st.session_state.track_index + 1) % len(tracks)
                st.rerun()
        with c5:
            # Цвет кнопки меняется, если трек в любимых
            heart = "💜" if current_file in st.session_state.favorites else "🤍"
            if st.button(heart):
                if current_file not in st.session_state.favorites:
                    st.session_state.favorites.append(current_file)
                    st.toast("В метедиатеке")
        st.markdown('</div>', unsafe_allow_html=True)

    # Аудиомодуль
    st.write("")
    st.audio(os.path.join(MUSIC_DIR, current_file))
