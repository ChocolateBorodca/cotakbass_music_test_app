import streamlit as st
import os

st.set_page_config(page_title="Liquid Glass Player", layout="wide")

# Ультра-дизайн Liquid Glass
st.markdown("""
    <style>
    /* Анимированный фон как на фото */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e, #000000);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: #FFFFFF;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Шрифты Apple */
    html, body, [class*="st-"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important;
    }

    /* Основная стеклянная карточка */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(50px) saturate(180%);
        -webkit-backdrop-filter: blur(50px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 40px;
        padding: 50px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        margin: auto;
        max-width: 600px;
        text-align: center;
    }

    /* Стеклянные кнопки-капли */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.07) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 50px !important; /* Круглые края как у капли */
        color: white !important;
        font-weight: 300 !important;
        height: 60px !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: inset 0 0 15px rgba(255,255,255,0.05);
    }
    div.stButton > button:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        transform: scale(1.1);
        box-shadow: 0 0 20px rgba(160, 100, 255, 0.3);
    }

    /* Текст */
    .track-title { 
        font-size: 48px; 
        font-weight: 700; 
        letter-spacing: -2px;
        background: linear-gradient(to bottom, #fff 0%, #aaa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .track-author { font-size: 22px; opacity: 0.4; font-weight: 300; margin-bottom: 40px; }
    
    /* Убираем лишний UI Streamlit */
    header {visibility: hidden;}
    .block-container {padding-top: 5rem !important;}
    </style>
    """, unsafe_allow_html=True)

# Логика треков
MUSIC_DIR = "music"
if not os.path.exists(MUSIC_DIR): os.makedirs(MUSIC_DIR)
tracks = sorted([f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")])

if 'page' not in st.session_state: st.session_state.page = "main"
if 'track_index' not in st.session_state: st.session_state.track_index = 0
if 'favorites' not in st.session_state: st.session_state.favorites = []

# Верхняя навигация (Библиотека)
c_nav, _ = st.columns([1, 4])
with c_nav:
    label = "← Назад" if st.session_state.page == "library" else " Библиотека"
    if st.button(label):
        st.session_state.page = "main" if st.session_state.page == "library" else "library"
        st.rerun()

if not tracks:
    st.info("Положи треки в папку music/")
else:
    current_file = tracks[st.session_state.track_index]

    if st.session_state.page == "library":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="track-title" style="font-size: 32px">Любимое</div>', unsafe_allow_html=True)
        for i, fav in enumerate(st.session_state.favorites):
            if st.button(f"✨ {fav.replace('.mp3', '')}", key=f"fav_{i}"):
                st.session_state.track_index = tracks.index(fav)
                st.session_state.page = "main"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        # Главный экран плеера
        display_name = current_file.replace(".mp3", "")
        author, title = display_name.split(" - ", 1) if " - " in display_name else ("Unknown", display_name)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="track-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="track-author">{author}</div>', unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("❮"):
                st.session_state.track_index = (st.session_state.track_index - 1) % len(tracks)
                st.rerun()
        with c2:
            st.button("▶")
        with c3:
            if st.button("❯"):
                st.session_state.track_index = (st.session_state.track_index + 1) % len(tracks)
                st.rerun()
        with c4:
            if st.button("♥"):
                if current_file not in st.session_state.favorites:
                    st.session_state.favorites.append(current_file)
                    st.toast("Сохранено в стекле")
        st.markdown('</div>', unsafe_allow_html=True)

    # Аудиомодуль (стилизованный)
    st.write("")
    st.audio(os.path.join(MUSIC_DIR, current_file))
