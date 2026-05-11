import streamlit as st
import os
import random
import base64
from PIL import Image

# Настройка страницы
st.set_page_config(page_title="cotakbass music", layout="wide", initial_sidebar_state="collapsed")

# Инициализация сессии
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user' not in st.session_state: st.session_state.user = {"name": "guest", "avatar": None}
if 'page' not in st.session_state: st.session_state.page = "main"

# Папки
for d in ["music", "avatars", "bg"]:
    if not os.path.exists(d): os.makedirs(d)

# CSS: Твой стиль + новые элементы
st.markdown(f"""
    <style>
    header, footer, #MainMenu {{ visibility: hidden !important; }}
    .stApp {{ background-color: #000000; color: #FFFFFF; font-family: -apple-system, sans-serif; }}
    
    /* Стеклянный блок входа */
    .glass-auth {{
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(50px);
        border: 1px solid rgba(160, 32, 240, 0.2);
        border-radius: 40px;
        padding: 50px 20px;
        text-align: center;
    }}

    /* Аватарка в профиле */
    .profile-circle {{
        width: 120px; height: 120px;
        border-radius: 50%;
        border: 3px solid #A020F0;
        object-fit: cover;
        margin-bottom: 20px;
    }}
    
    /* Кнопки как раньше */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(160, 32, 240, 0.2) !important;
        border-radius: 50px !important;
        color: white !important;
        transition: 0.3s ease;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 1. ЭКРАН ВХОДА ---
def show_auth():
    st.markdown('<div style="text-align:center; color:#A020F0; font-size:28px; letter-spacing:8px; margin: 40px 0;">cotakbass music</div>', unsafe_allow_html=True)
    
    _, col, _ = st.columns([0.1, 0.8, 0.1])
    with col:
        st.markdown('<div class="glass-auth">', unsafe_allow_html=True)
        st.subheader("регистрация")
        
        name = st.text_input("твой ник", placeholder="как тебя зовут?")
        bio = st.text_area("о себе", placeholder="пару слов...")
        ava = st.file_uploader("загрузи аватарку", type=['png', 'jpg'])
        
        if st.button("войти в систему"):
            if name:
                st.session_state.user['name'] = name
                if ava:
                    with open(f"avatars/{name}.png", "wb") as f:
                        f.write(ava.getbuffer())
                    st.session_state.user['avatar'] = f"avatars/{name}.png"
                st.session_state.auth = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 2. ЭКРАН ПРОФИЛЯ (SOUNDCLOUD STYLE) ---
def show_profile():
    st.markdown('<div style="text-align:center; color:#A020F0; font-size:10px; letter-spacing:5px;">profile</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
    with col2:
        if st.session_state.user['avatar']:
            st.image(st.session_state.user['avatar'], width=150)
        st.title(st.session_state.user['name'])
        st.write("---")
        
        st.subheader("опубликовать трек")
        new_track = st.file_uploader("выбери .mp3", type="mp3")
        track_name = st.text_input("название трека")
        
        if st.button("опубликовать") and new_track and track_name:
            with open(f"music/{st.session_state.user['name']} - {track_name}.mp3", "wb") as f:
                f.write(new_track.getbuffer())
            st.success("трек загружен!")

# --- ЗАПУСК ПРИЛОЖЕНИЯ ---
if not st.session_state.auth:
    show_auth()
else:
    # Навигация: Ава | Пусто | Поиск
    n1, n2, n3 = st.columns([0.2, 0.6, 0.2])
    with n1:
        # Индикатор сети вокруг авы (упрощенно кнопкой)
        if st.button("👤"): 
            st.session_state.page = "profile" if st.session_state.page != "profile" else "main"
            st.rerun()
    with n3:
        if st.button("?"): 
            st.session_state.page = "search"
            st.rerun()

    if st.session_state.page == "profile":
        show_profile()
    elif st.session_state.page == "main":
        st.markdown('<div style="text-align:center; margin-top:20vh;">', unsafe_allow_html=True)
        st.markdown(f"<h2>привет, {st.session_state.user['name']}</h2>", unsafe_allow_html=True)
        st.write("твой плеер готов к работе")
        st.markdown('</div>', unsafe_allow_html=True)
        # Сюда вставляется код плеера
