import streamlit as st
import os
import json

# Настройка стиля Apple + SoundCloud
st.set_page_config(page_title="cotakbass", layout="wide", initial_sidebar_state="collapsed")

# Создание папок
for d in ["music", "avatars", "bg_profiles"]:
    if not os.path.exists(d): os.makedirs(d)

# CSS для индикатора сети и стеклянного профиля
st.markdown(f"""
    <style>
    /* Индикатор сети вокруг авы */
    .online-indicator {{
        border: 3px solid #A020F0 !important; /* Фиолетовый - в сети */
        padding: 5px;
        border-radius: 50%;
        display: inline-block;
    }}
    .offline-indicator {{
        border: 3px solid #333 !important; /* Черный - оффлайн */
        padding: 5px;
        border-radius: 50%;
        display: inline-block;
    }}
    
    /* Скрытие мусора */
    header, footer, #MainMenu {{ visibility: hidden !important; }}
    .stApp {{ background-color: #000000; color: white; }}
    </style>
""", unsafe_allow_html=True)

# Логика регистрации/входа
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    # Экран входа (твой минимализм)
    st.markdown("<h1 style='text-align:center; color:#A020F0;'>cotakbass music</h1>", unsafe_allow_html=True)
    with st.container():
        name = st.text_input("Никнейм")
        ava = st.file_uploader("Загрузи аватарку", type=['png', 'jpg'])
        if st.button("Войти"):
            if name:
                st.session_state.auth = True
                st.session_state.user = name
                st.rerun()
else:
    # Главный экран
    col_ava, col_space, col_search = st.columns([0.1, 0.8, 0.1])
    
    with col_ava:
        # Аватарка с фиолетовой линией (если в сети)
        st.markdown('<div class="online-indicator">👤</div>', unsafe_allow_html=True)
        if st.button("Профиль"):
            st.session_state.page = "profile"
    
    with col_search:
        if st.button("🔍"):
            st.session_state.page = "search"

    # Страница публикации (как в SoundCloud)
    if st.session_state.get('page') == "profile":
        st.subheader("Мой Профиль")
        uploaded_track = st.file_uploader("Опубликовать свой трек", type="mp3")
        track_title = st.text_input("Название трека")
        
        if st.button("Опубликовать") and uploaded_track:
            # Сохраняем файл в папку music
            with open(os.path.join("music", f"{st.session_state.user}_{track_title}.mp3"), "wb") as f:
                f.write(uploaded_track.getbuffer())
            st.success("Трек опубликован и доступен в поиске!")
