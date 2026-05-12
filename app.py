import streamlit as st
import os
import random
import base64

# --- 1. НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="cotakbass music", layout="wide", initial_sidebar_state="collapsed")

# Создание необходимых папок
for d in ["music", "bg", "avatars"]:
    if not os.path.exists(d): os.makedirs(d)

# --- 2. ИНИЦИАЛИЗАЦИЯ СОСТОЯНИЯ (SESSION STATE) ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user' not in st.session_state or not isinstance(st.session_state.user, dict):
    st.session_state.user = {"name": "", "status": "", "ava": None}
if 'page' not in st.session_state: st.session_state.page = "main"
if 'track_index' not in st.session_state: st.session_state.track_index = 0
if 'favorites' not in st.session_state: st.session_state.favorites = set()
if 'playing' not in st.session_state: st.session_state.playing = False
if 'current_bg' not in st.session_state: st.session_state.current_bg = None

# Вспомогательная функция для картинок
def get_base64(file):
    return base64.b64encode(file.getvalue()).decode() if file else None

# --- 3. ГЛОБАЛЬНЫЕ СТИЛИ (APPLE + OLED + NO DOTS) ---
bg_css = "background-color: #000000;"
bg_gifs = [f for f in os.listdir("bg") if f.endswith(".gif")]
if st.session_state.playing and bg_gifs:
    if st.session_state.current_bg is None:
        st.session_state.current_bg = random.choice(bg_gifs)
    try:
        with open(os.path.join("bg", st.session_state.current_bg), "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        bg_css = f'background-image: url("data:image/gif;base64,{encoded}"); background-size: cover; background-position: center;'
    except: pass

online_glow = "box-shadow: 0 0 20px #A020F0; border: 2px solid #A020F0 !important;" if st.session_state.auth else "border: 1px solid rgba(255,255,255,0.1) !important;"

st.markdown(f"""
    <style>
    /* Полная зачистка системного мусора Streamlit */
    header, footer, #MainMenu, [data-testid="stInputInstructions"], 
    .st-emotion-cache-oc994i, .st-emotion-cache-1pxm666, .st-emotion-cache-1vt4y65 {{
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }}
    
    html, body, [class*="st-"] {{ font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important; }}
    .stApp {{ {bg_css} transition: background 0.8s ease; }}
    .stApp::before {{ content: ""; position: absolute; inset: 0; background: rgba(0, 0, 0, 0.88); z-index: -1; }}
    audio {{ display: none !important; }}

    /* Стеклянные кнопки */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(40px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 50% !important;
        color: #A020F0 !important;
        width: 55px !important; height: 55px !important;
        transition: 0.3s ease;
        display: flex; align-items: center; justify-content: center;
    }}
    
    /* Свечение иконки профиля в плеере */
    .nav-profile-btn button {{ {online_glow} }}

    /* ЗОНА ЗАГРУЗКИ АВАТАРКИ (РЕГИСТРАЦИЯ) */
    .upload-wrapper {{
        position: relative;
        width: 140px; height: 140px;
        margin: 40px auto;
        display: flex; align-items: center; justify-content: center;
    }}
    /* Растягиваем невидимый загрузчик на весь круг */
    [data-testid="stFileUploader"] {{
        position: absolute !important;
        inset: 0 !important;
        width: 100% !important; height: 100% !important;
        opacity: 0 !important; z-index: 1000 !important;
        cursor: pointer !important;
    }}
    .ava-visual-circle {{
        width: 100%; height: 100%;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(30px);
        border: 2px solid #A020F0;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 40px; color: #A020F0;
        overflow: hidden;
        position: relative;
    }}
    .ava-preview-img {{ width: 100%; height: 100%; object-fit: cover; position: absolute; inset: 0; }}

    /* Поля ввода (Капсулы) */
    div[data-testid="stTextInput"] div[data-baseweb="input"] {{
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 25px !important;
        max-width: 350px; margin: 0 auto;
    }}
    div[data-testid="stTextInput"] input {{ text-align: center !important; color: white !important; padding: 12px !important; }}
    div[data-testid="stTextInput"] label {{ display: none !important; }}

    /* НАЗВАНИЕ ТРЕКА СЛЕВА */
    .track-info-left {{ text-align: left; padding-left: 5%; margin-top: 10vh; }}
    .title-text {{ font-size: 44px; font-weight: 800; color: white; letter-spacing: -1.5px; line-height: 1; }}
    .author-text {{ font-size: 18px; color: #A020F0; font-weight: 300; margin-top: 5px; margin-bottom: 60px; }}

    /* ПОИСК С "?" ВНУТРИ */
    .search-box-style div[data-baseweb="input"]::after {{
        content: "?"; position: absolute; right: 20px; top: 50%; transform: translateY(-50%);
        color: #A020F0; font-weight: 700; font-size: 18px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. ЛОГИКА ЭКРАНОВ ---

# ЭКРАН РЕГИСТРАЦИИ
if not st.session_state.auth:
    st.markdown('<h1 style="text-align:center; font-weight:200; margin-top:30px;">cotakbass</h1>', unsafe_allow_html=True)
    
    # КРУГ АВАТАРКИ
    st.markdown('<div class="upload-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="ava-visual-circle">', unsafe_allow_html=True)
    u_ava = st.file_uploader("", key="reg_ava_up")
    img_data = get_base64(u_ava)
    if img_data:
        st.markdown(f'<img src="data:image/png;base64,{img_data}" class="ava-preview-img">', unsafe_allow_html=True)
        st.session_state.user['ava'] = img_data
    else:
        st.write("+")
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # ПОЛЯ ВВОДА
    u_name = st.text_input("name", placeholder="name", key="reg_name")
    u_status = st.text_input("status", placeholder="status", key="reg_status")
    
    # КНОПКА ДВЕРЬ (ЦЕНТР)
    st.markdown('<div style="display:flex; justify-content:center; margin-top:40px;">', unsafe_allow_html=True)
    if st.button("🚪"):
        if u_name:
            st.session_state.auth = True
            st.session_state.user['name'] = u_name
            st.session_state.user['status'] = u_status
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ГЛАВНЫЙ ЭКРАН ПЛЕЕРА
else:
    # Навигация (☰ | 👤 | ?)
    n1, _, n2, n3 = st.columns([0.15, 0.6, 0.12, 0.13])
    with n1:
        if st.button("☰"): st.session_state.page = "library"; st.rerun()
    with n2:
        st.markdown('<div class="nav-profile-btn">', unsafe_allow_html=True)
        if st.button("👤"): st.session_state.page = "profile"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with n3:
        if st.button("?"): st.session_state.page = "search"; st.rerun()

    tracks = sorted([f for f in os.listdir("music") if f.endswith(".mp3")])
    
    if st.session_state.page == "search":
        st.markdown('<div class="search-box-style">', unsafe_allow_html=True)
        q = st.text_input("", placeholder="напиши хуйню", key="search_q")
        st.markdown('</div>', unsafe_allow_html=True)
        if q:
            for t in [x for x in tracks if q.lower() in x.lower()]:
                c_n, c_p = st.columns([0.85, 0.15])
                with c_n: st.markdown(f"<div style='color:white; padding:15px 0; border-bottom:1px solid #111;'>{t.replace('.mp3','')}</div>", unsafe_allow_html=True)
                with c_p:
                    if st.button("▶", key=f"s_{t}"):
                        st.session_state.track_index, st.session_state.page, st.session_state.playing = tracks.index(t), "main", True; st.rerun()

    elif st.session_state.page == "library":
        st.markdown('<div style="text-align:center; opacity:0.5; font-size:10px; letter-spacing:5px;">FAVORITES</div>', unsafe_allow_html=True)
        for f in list(st.session_state.favorites):
            c_n, c_p = st.columns([0.85, 0.15])
            with c_n: st.markdown(f"<div style='color:white; padding:15px 0; border-bottom:1px solid #111;'>{f.replace('.mp3','')}</div>", unsafe_allow_html=True)
            with c_p:
                if st.button("▶", key=f"l_{f}"):
                    st.session_state.track_index, st.session_state.page, st.session_state.playing = tracks.index(f), "main", True; st.rerun()

    elif st.session_state.page == "profile":
        # Экран Профиля (SoundCloud Style)
        st.markdown(f"""
            <div style="text-align:center; margin-top:5vh;">
                <img src="data:image/png;base64,{st.session_state.user['ava'] if st.session_state.user['ava'] else ''}" style="width:120px; height:120px; border-radius:50%; border:2px solid #A020F0; object-fit:cover;">
                <h2 style="margin-top:15px;">{st.session_state.user['name']}</h2>
                <p style="opacity:0.6;">{st.session_state.user['status']}</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("← back"): st.session_state.page = "main"; st.rerun()
        st.write("---")
        st.subheader("Опубликовать трек")
        new_mp3 = st.file_uploader("выбери mp3", type="mp3")
        if st.button("upload") and new_mp3:
            with open(os.path.join("music", new_mp3.name), "wb") as f: f.write(new_mp3.getbuffer())
            st.success("done!")

    else:
        # ОСНОВНОЙ ПЛЕЕР
        if tracks:
            st.markdown('<div style="text-align:center; opacity:0.5; font-size:10px; letter-spacing:4px;">COTAKBASS MUSIC</div>', unsafe_allow_html=True)
            curr = tracks[st.session_state.track_index]
            name_c = curr.replace(".mp3", "").replace("_", " ")
            auth, title = name_c.split(", ", 1) if ", " in name_c else ("unknown", name_c)
            st.markdown(f'<div class="track-info-left"><div class="title-text">{title}</div><div class="author-text">{auth}</div></div>', unsafe_allow_html=True)
            _, b1, b2, b3, b4, _ = st.columns(6)
            with b1:
                if st.button("❮"): st.session_state.track_index = (st.session_state.track_index - 1) % len(tracks); st.session_state.current_bg = None; st.rerun()
            with b2:
                if st.button("Ⅱ" if st.session_state.playing else "▶"): st.session_state.playing = not st.session_state.playing; st.rerun()
            with b3:
                if st.button("❯"): st.session_state.track_index = (st.session_state.track_index + 1) % len(tracks); st.session_state.current_bg = None; st.rerun()
            with b4:
                is_f = curr in st.session_state.favorites
                if st.button("💜" if is_f else "🤍"):
                    if is_f: st.session_state.favorites.remove(curr)
                    else: st.session_state.favorites.add(curr); st.snow()
                    st.rerun()
            st.audio(os.path.join("music", curr), autoplay=st.session_state.playing)
