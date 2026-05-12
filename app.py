import streamlit as st
import os
import random
import base64

# --- 1. НАСТРОЙКИ ---
st.set_page_config(page_title="cotakbass", layout="wide", initial_sidebar_state="collapsed")

def get_base64(file):
    return base64.b64encode(file.getvalue()).decode() if file else None

if 'user_ava' not in st.session_state: st.session_state.user_ava = None
if 'page' not in st.session_state: st.session_state.page = "main"
if 'playing' not in st.session_state: st.session_state.playing = False
if 'track_index' not in st.session_state: st.session_state.track_index = 0
if 'favorites' not in st.session_state: st.session_state.favorites = set()
if 'current_bg' not in st.session_state: st.session_state.current_bg = None

# --- 2. ОБЩИЙ CSS (ЗАЧИСТКА ВСЕГО) ---
st.markdown(f"""
    <style>
    /* Полная зачистка мусора */
    header, footer, #MainMenu, [data-testid="stInputInstructions"], 
    .st-emotion-cache-oc994i, .st-emotion-cache-1vt4y65, .st-emotion-cache-k7vsyb,
    [data-testid="stHeader"], [data-testid="stFileUploaderDeleteBtn"],
    .st-emotion-cache-6q9sum, .st-emotion-cache-10trblm {{
        display: none !important;
    }}
    .stApp {{ background-color: #000000; }}
    .stApp::before {{ content: ""; position: absolute; inset: 0; background: rgba(0, 0, 0, 0.85); z-index: -1; }}
    audio {{ display: none !important; }}

    /* Кнопки плеера */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(40px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 50% !important;
        color: #A020F0 !important;
        transition: 0.3s ease;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. ЛОГИКА ЭКРАНОВ ---

if st.session_state.page == "profile":
    # СТИЛИ ТОЛЬКО ДЛЯ ПРОФИЛЯ
    st.markdown("""
        <style>
        .back-btn-fixed { position: fixed; top: 30px; left: 30px; z-index: 9999; }
        
        /* КРУГ РОВНО В ЦЕНТРЕ */
        .circle-wrapper {
            position: fixed; top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            width: 220px; height: 220px;
            z-index: 1000;
            display: flex; align-items: center; justify-content: center;
        }

        .visual-circle {
            width: 200px; height: 200px;
            border-radius: 50%; border: 2px solid #A020F0;
            background: rgba(160, 32, 240, 0.05);
            backdrop-filter: blur(30px);
            display: flex; align-items: center; justify-content: center;
            font-size: 50px; color: #A020F0; overflow: hidden;
            box-shadow: 0 0 50px rgba(160, 32, 240, 0.2);
        }
        .visual-circle img { width: 100%; height: 100%; object-fit: cover; }

        /* РАБОЧИЙ ЗАГРУЗЧИК ПОВЕРХ КРУГА */
        [data-testid="stFileUploader"] {
            position: fixed !important;
            top: 50% !important; left: 50% !important;
            transform: translate(-50%, -50%) !important;
            width: 200px !important; height: 200px !important;
            opacity: 0 !important; z-index: 1100 !important;
            cursor: pointer !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Кнопка назад в углу
    st.markdown('<div class="back-btn-fixed">', unsafe_allow_html=True)
    if st.button("←", key="exit_p"):
        st.session_state.page = "main"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Визуал круга
    st.markdown('<div class="circle-wrapper">', unsafe_allow_html=True)
    if st.session_state.user_ava:
        st.markdown(f'<div class="visual-circle"><img src="data:image/png;base64,{st.session_state.user_ava}"></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="visual-circle">+</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Сам загрузчик (невидимый, но кликабельный)
    up = st.file_uploader("", key="ava_up", label_visibility="collapsed")
    if up:
        st.session_state.user_ava = get_base64(up)
        st.rerun()

else:
    # --- ГЛАВНЫЙ ЭКРАН ПЛЕЕРА ---
    # Динамический фон
    bg_style = ""
    if st.session_state.playing:
        bg_gifs = [f for f in os.listdir("bg") if f.endswith(".gif")] if os.path.exists("bg") else []
        if bg_gifs:
            if st.session_state.current_bg is None: st.session_state.current_bg = random.choice(bg_gifs)
            try:
                with open(os.path.join("bg", st.session_state.current_bg), "rb") as f:
                    encoded = base64.b64encode(f.read()).decode()
                bg_style = f'background-image: url("data:image/gif;base64,{encoded}"); background-size: cover; background-position: center;'
            except: pass
    
    st.markdown(f'<style>.stApp {{ {bg_style if bg_style else "background-color: #000000;"} }}</style>', unsafe_allow_html=True)

    # Навигация
    n1, _, n2, n3 = st.columns([0.15, 0.6, 0.12, 0.13])
    with n1:
        if st.button("☰"): st.session_state.page = "library" if st.session_state.page != "library" else "main"; st.rerun()
    with n2:
        glow = "box-shadow: 0 0 15px #A020F0; border: 2px solid #A020F0 !important;" if st.session_state.user_ava else ""
        st.markdown(f'<div style="{glow} border-radius:50%; width:55px; height:55px;">', unsafe_allow_html=True)
        if st.button("👤"): st.session_state.page = "profile"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with n3:
        if st.button("?"): st.session_state.page = "search"; st.rerun()

    tracks = sorted([f for f in os.listdir("music") if f.endswith(".mp3")]) if os.listdir("music") else []

    if st.session_state.page == "search":
        q = st.text_input("", placeholder="напиши хуйню", key="s_q")
        if q and tracks:
            for t in [x for x in tracks if q.lower() in x.lower()]:
                c_n, c_p = st.columns([0.85, 0.15])
                with c_n: st.markdown(f"<div style='color:white; padding:15px 0; border-bottom:1px solid #111;'>{t.replace('.mp3','')}</div>", unsafe_allow_html=True)
                with c_p:
                    if st.button("▶", key=f"s_{t}"):
                        st.session_state.track_index, st.session_state.page, st.session_state.playing = tracks.index(t), "main", True; st.rerun()
    
    elif st.session_state.page == "library":
        st.markdown('<div style="text-align:center; color:#A020F0; letter-spacing:5px; margin-top:20px;">FAVORITES</div>', unsafe_allow_html=True)
        for f in list(st.session_state.favorites):
            c_n, c_p = st.columns([0.85, 0.15])
            with c_n: st.markdown(f"<div style='color:white; padding:15px 0; border-bottom:1px solid #111;'>{f.replace('.mp3','')}</div>", unsafe_allow_html=True)
            with c_p:
                if st.button("▶", key=f"l_{f}"):
                    st.session_state.track_index, st.session_state.page, st.session_state.playing = tracks.index(f), "main", True; st.rerun()
    
    elif tracks:
        # Плеер
        curr = tracks[st.session_state.track_index]
        name_c = curr.replace(".mp3", "").replace("_", " ")
        auth, title = name_c.split(", ", 1) if ", " in name_c else ("unknown", name_c)
        st.markdown(f'<div style="text-align:left; padding-left:5%; margin-top:15vh;"><div style="font-size:44px; font-weight:800; color:white; letter-spacing:-2px;">{title}</div><div style="font-size:18px; color:#A020F0; font-weight:300; margin-top:10px; margin-bottom:60px;">{auth}</div></div>', unsafe_allow_html=True)
        
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
