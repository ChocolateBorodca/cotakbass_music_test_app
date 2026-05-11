import streamlit as st
import os
import random
import base64
from components.auth import registration_screen, profile_screen

# Настройка
st.set_page_config(page_title="cotakbass music", layout="wide", initial_sidebar_state="collapsed")

MUSIC_DIR, BG_DIR = "music", "bg"
for d in [MUSIC_DIR, BG_DIR]:
    if not os.path.exists(d): os.makedirs(d)

# Session State
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user' not in st.session_state: st.session_state.user = {"name": "guest", "bio": "", "ava": None}
if 'page' not in st.session_state: st.session_state.page = "main"
if 'track_index' not in st.session_state: st.session_state.track_index = 0
if 'favorites' not in st.session_state: st.session_state.favorites = set()
if 'playing' not in st.session_state: st.session_state.playing = False
if 'current_bg' not in st.session_state: st.session_state.current_bg = None

# СТИЛИ С ФИОЛЕТОВЫМ ГЛОУ
online_glow = "box-shadow: 0 0 15px #A020F0; border: 2px solid #A020F0 !important;" if st.session_state.auth else ""

st.markdown(f"""
    <style>
    header, footer, #MainMenu {{ display: none !important; }}
    .stApp {{ background-color: #000000; color: white; }}
    
    /* Кнопка Профиля со свечением */
    .profile-btn button {{
        {online_glow}
        border-radius: 50% !important;
        width: 55px !important; height: 55px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ЛОГИКА ЭКРАНОВ
if st.session_state.page == "registration":
    registration_screen()
elif st.session_state.page == "profile":
    profile_screen()
else:
    # ТВОЙ ПЛЕЕР (Навигация)
    n1, _, n2, n3 = st.columns([0.15, 0.6, 0.12, 0.13])
    with n1:
        if st.button("☰"): st.session_state.page = "library"; st.rerun()
    with n2:
        st.markdown('<div class="profile-btn">', unsafe_allow_html=True)
        if st.button("👤"): 
            st.session_state.page = "profile" if st.session_state.auth else "registration"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with n3:
        if st.button("?"): st.session_state.page = "search"; st.rerun()

    # --- ТВОЙ ОСНОВНОЙ КОД ПЛЕЕРА ДАЛЬШЕ ---
    # (Оставь здесь логику отображения треков и кнопки ❮ ▶ ❯ из твоего app.py)
    st.write(f"<div style='text-align:left; padding-left:5%; margin-top:10vh; font-size:42px; font-weight:700;'>playing tracks...</div>", unsafe_allow_html=True)
