import streamlit as st
import os
import random
import base64

# Настройка страницы
st.set_page_config(page_title="cotakbass music", layout="wide", initial_sidebar_state="collapsed")

# Папки
MUSIC_DIR, BG_DIR = "music", "bg"
for d in [MUSIC_DIR, BG_DIR]:
    if not os.path.exists(d): os.makedirs(d)

# Session State
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'page' not in st.session_state: st.session_state.page = "main"
if 'track_index' not in st.session_state: st.session_state.track_index = 0
if 'favorites' not in st.session_state: st.session_state.favorites = set()
if 'playing' not in st.session_state: st.session_state.playing = False
if 'current_bg' not in st.session_state: st.session_state.current_bg = None

def get_base64_img(file):
    if file: return base64.b64encode(file.getvalue()).decode()
    return None

# --- 1. ЭКРАН РЕГИСТРАЦИИ (ФИКС ГАЛЕРЕИ) ---
def registration_screen():
    st.markdown(f"""
        <style>
        header, footer, #MainMenu, [data-testid="stInputInstructions"] {{ display: none !important; }}
        .stApp {{ background-color: #000000; color: #FFFFFF; font-family: -apple-system, sans-serif; }}
        
        /* ГЛАВНЫЙ ФИКС ГАЛЕРЕИ: Растягиваем невидимый клик на всю площадь */
        div[data-testid="stFileUploader"] {{
            position: absolute !important;
            inset: 0 !important;
            width: 100% !important;
            height: 100% !important;
            z-index: 500 !important;
        }}
        div[data-testid="stFileUploader"] section {{
            padding: 0 !important;
            min-height: 100% !important;
            background: transparent !important;
            border: none !important;
            opacity: 0 !important; /* Полная невидимость */
        }}
        /* Убираем лишние кнопки внутри скрытого загрузчика */
        div[data-testid="stFileUploader"] button {{ display: none !important; }}

        /* Прямоугольник (ФОН) */
        .bg-box {{ 
            background: rgba(255,255,255,0.03); 
            backdrop-filter: blur(40px); 
            border: 1px solid rgba(255,255,255,0.1); 
            border-radius: 25px; 
            height: 140px; width: 100%; max-width: 480px; 
            margin: 0 auto; 
            display: flex; align-items: center; justify-content: center; 
            font-size: 32px; color: rgba(160, 32, 240, 0.4); 
            position: relative;
        }}

        /* Круг (АВАТАРКА) */
        .ava-circle {{ 
            width: 120px; height: 120px; 
            background: rgba(255, 255, 255, 0.05); 
            backdrop-filter: blur(30px); 
            border: 2px solid #A020F0; 
            border-radius: 50%; 
            margin: -60px auto 30px auto; 
            display: flex; align-items: center; justify-content: center; 
            font-size: 32px; color: #A020F0; 
            position: relative; 
            z-index: 10;
            overflow: hidden;
        }}
        .preview-img {{ width: 100%; height: 100%; object-fit: cover; position: absolute; inset: 0; }}
        
        /* Поля ввода */
        div[data-testid="stTextInput"] div[data-baseweb="input"] {{ 
            background: rgba(255, 255, 255, 0.04) !important; 
            border-radius: 30px !important; 
            max-width: 350px; margin: 0 auto; 
            border: 1px solid rgba(255,255,255,0.1) !important; 
        }}
        div[data-testid="stTextInput"] input {{ text-align: center !important; color: white !important; padding: 12px !important; }}
        div[data-testid="stTextInput"] label {{ display: none !important; }}

        /* Кнопка стрелка */
        div.stButton > button {{ 
            background: rgba(255, 255, 255, 0.02) !important; 
            border: 1px solid rgba(160, 32, 240, 0.4) !important; 
            border-radius: 50% !important; 
            color: #A020F0 !important; 
            width: 65px !important; height: 65px !important; 
            font-size: 28px !important; 
            margin: 30px auto !important; display: block !important; 
        }}
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="draw-title" style="text-align:center; font-size:40px; margin-top:20px; font-weight:200;">cotakbass</div>', unsafe_allow_html=True)
    
    # ЗОНА ФОНА (Прямоугольник)
    st.markdown('<div class="bg-box">', unsafe_allow_html=True)
    st.file_uploader("", key="u_bg")
    st.write("+")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ЗОНА АВАТАРКИ (Круг)
    st.markdown('<div class="ava-circle">', unsafe_allow_html=True)
    u_ava = st.file_uploader("", key="u_ava")
    base64_ava = get_base64_img(u_ava)
    if base64_ava:
        st.markdown(f'<img src="data:image/png;base64,{base64_ava}" class="preview-img">', unsafe_allow_html=True)
    else:
        st.write("+")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Инпуты
    st.write("<div style='height:20px'></div>", unsafe_allow_html=True)
    name = st.text_input("name", placeholder="name", key="reg_n")
    status = st.text_input("status", placeholder="status", key="reg_s")
    
    if st.button("❯"):
        if name:
            st.session_state.auth = True
            st.session_state.user_name = name
            st.rerun()

# --- 2. ПЛЕЕР ---
def main_player():
    tracks = sorted([f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")])
    bg_gifs = [f for f in os.listdir(BG_DIR) if f.endswith(".gif")]

    bg_html = "background-color: #000000;"
    if st.session_state.playing and bg_gifs:
        if st.session_state.current_bg is None:
            st.session_state.current_bg = random.choice(bg_gifs)
        try:
            with open(os.path.join(BG_DIR, st.session_state.current_bg), "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            bg_html = f'background-image: url("data:image/gif;base64,{encoded}"); background-size: cover; background-position: center;'
        except: pass

    st.markdown(f"""
        <style>
        header, footer, #MainMenu, [data-testid="stInputInstructions"], .st-emotion-cache-1pxm666 {{ display: none !important; }}
        .stApp {{ {bg_html} transition: background 0.8s ease; }}
        .stApp::before {{ content: ""; position: absolute; inset: 0; background: rgba(0, 0, 0, 0.85); z-index: -1; }}
        audio {{ display: none !important; }}
        div.stButton > button {{ background: rgba(255, 255, 255, 0.02) !important; backdrop-filter: blur(30px) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 50% !important; color: white !important; width: 55px !important; height: 55px !important; transition: 0.3s ease; }}
        .search-title {{ font-size: 14px; letter-spacing: 8px; color: #A020F0; text-align: center; margin-bottom: 30px; }}
        div[data-testid="stTextInput"] div[data-baseweb="input"] {{ background: rgba(255, 255, 255, 0.03) !important; backdrop-filter: blur(60px) brightness(0.7) !important; border: 1px solid rgba(160, 32, 240, 0.2) !important; border-radius: 22px !important; position: relative; }}
        div[data-testid="stTextInput"] div[data-baseweb="input"]::after {{ content: "?"; position: absolute; right: 20px; top: 50%; transform: translateY(-50%); color: #A020F0; font-weight: 700; }}
        </style>
    """, unsafe_allow_html=True)

    n1, _, n2 = st.columns([0.15, 0.7, 0.15])
    with n1:
        if st.button("←" if st.session_state.page != "main" else "☰"):
            st.session_state.page = "main" if st.session_state.page != "main" else "library"; st.rerun()
    with n2:
        if st.button("?"): st.session_state.page = "search"; st.rerun()

    if not tracks:
        st.info("No tracks")
    else:
        if st.session_state.page == "search":
            st.markdown('<div class="search-title">search</div>', unsafe_allow_html=True)
            query = st.text_input("", placeholder="напиши хуйню", key="search_input")
            if query:
                for t in [x for x in tracks if query.lower() in x.lower()]:
                    c1, c2 = st.columns([0.85, 0.15])
                    with c1: st.markdown(f"<div style='padding:18px 0; border-bottom:1px solid rgba(255,255,255,0.02);'>{t.replace('.mp3', '')}</div>", unsafe_allow_html=True)
                    with c2:
                        if st.button("▶", key=f"s_{t}"): st.session_state.track_index, st.session_state.page, st.session_state.playing = tracks.index(t), "main", True; st.rerun()
        elif st.session_state.page == "library":
            st.markdown('<div style="text-align:center; opacity:0.5; font-size:10px; letter-spacing:5px;">FAVORITES</div>', unsafe_allow_html=True)
            for fav in list(st.session_state.favorites):
                c1, c2 = st.columns([0.85, 0.15])
                with c1: st.markdown(f"<div style='padding:18px 0; border-bottom:1px solid rgba(255,255,255,0.02);'>{fav.replace('.mp3', '')}</div>", unsafe_allow_html=True)
                with c2:
                    if st.button("▶", key=f"f_{fav}"): st.session_state.track_index, st.session_state.page, st.session_state.playing = tracks.index(fav), "main", True; st.rerun()
        else:
            st.markdown('<div style="text-align:center; opacity:0.5; font-size:10px; letter-spacing:4px; margin-top:20px;">COTAKBASS MUSIC</div>', unsafe_allow_html=True)
            curr = tracks[st.session_state.track_index]
            auth, title = curr.replace(".mp3", "").split(", ", 1) if ", " in curr else ("unknown", curr.replace(".mp3", ""))
            st.markdown(f'<div style="text-align:center; margin-top:10vh;"><div style="font-size:42px; font-weight:700;">{title}</div><div style="color:#A020F0; font-size:18px; margin-bottom:50px;">{auth}</div></div>', unsafe_allow_html=True)
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
            st.audio(os.path.join(MUSIC_DIR, curr), autoplay=st.session_state.playing)

# --- ЗАПУСК ---
if not st.session_state.auth: registration_screen()
else: main_player()
