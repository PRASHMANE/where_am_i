import streamlit as st
from add_info import add,add_student,get_all_students,get_student_by_roll,goto,update_student,remove_student
from cam import webcam
from pathlib import Path
import streamlit as st
import sqlite3
from sqlite3 import Connection
from datetime import datetime
import time
from home import home
from dashboard import dashboard
import cv2
import numpy as np
from insightface.app import FaceAnalysis
import os
from src.models.model import load_known_faces

DB_PATH = "students.db"
PHOTOS_DIR = Path("data")
PHOTOS_DIR.mkdir(exist_ok=True)


# --- Page setup ---
st.set_page_config(page_title="Dark Theme App", layout="wide")

# --- Load Material Icons ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined"
          rel="stylesheet" />
""", unsafe_allow_html=True)

# --- Dark Theme CSS ---
st.markdown("""
    <style>
    /* === Full Screen Dark Background === */
    html, body, [class*="stApp"], .main, .block-container {
        background-color: #0d1117 !important; /* deep dark gray */
        color: #e6edf3 !important; /* light text for readability */
    }

    /* Widget styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > input {
        background-color: #161b22 !important; 
        color: #e6edf3 !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        padding: 0.5rem 0.75rem !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #00bfa5, #00ffcc) !important;
        color: black !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        transition: 0.3s ease-in-out;
        font-weight: 600;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px #00ffcc;
    }

    /* Bottom Navigation */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #161b22;
        border-top: 1px solid #30363d;
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 14px 0;
        z-index: 100;
    }

    .material-symbols-outlined {
        font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 48;
        font-size: 30px;
        color: #8b949e;
        cursor: pointer;
        transition: all 0.3s ease-in-out;
        padding: 8px;
        border-radius: 50%;
    }
    .material-symbols-outlined:hover {
        color: #00ffcc;
        transform: scale(1.2);
        text-shadow: 0 0 12px #00bfa5;
        background: rgba(0,255,204,0.15);
    }
    .active {
        color: #00ffcc !important;
        text-shadow: 0 0 16px #00ffcc;
        background: rgba(0,255,204,0.15);
        transform: scale(1.25);
    }

    body {
        margin-bottom: 90px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet" />
<style>
html, body, [class*="css"]  { font-family: 'Poppins', sans-serif; }
.appview-container .main .block-container{ padding-top:1rem; }
.card {
  background: rgba(255,255,255,0.05);
  border-radius: 12px;
  padding: 18px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.5);
  transition: transform .18s ease, box-shadow .18s ease;
}
.card:hover { transform: translateY(-6px); box-shadow: 0 12px 30px rgba(0,255,204,0.2); }
.btn-glow {
  border-radius: 10px;
  padding: 10px 14px;
  font-weight:600;
  box-shadow: 0 6px 20px rgba(0,255,204,0.12);
}
.small-muted { color: #9aa0a6; font-size:13px; }
.material {
  vertical-align: middle;
  font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
  margin-right:6px;
}
.logo {
  display:inline-flex; align-items:center; gap:10px; margin-bottom:6px;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
.card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    padding: 20px 30px;
    margin-bottom: 20px;
    text-align: center;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 20px rgba(0, 255, 204, 0.2);
    color: #00ffcc;
    border: 1px solid rgba(0, 255, 204, 0.2);
}

.stTextInput>div>div>input {
    background: rgba(255,255,255,0.05);
    color: #fff;
    border: 2px solid #00ffcc;
    border-radius: 10px;
    padding: 10px;
}

.stButton>button {
    background: linear-gradient(135deg, #00ffcc, #00bfa5);
    color: black;
    border-radius: 30px;
    padding: 0.7rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    border: none;
    box-shadow: 0 0 20px #00ffcc, 0 0 40px #00bfa5;
    transition: all 0.3s ease-in-out;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)


# --- Initialize page state ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Handle navigation ---
query_params = st.query_params
if "page" in query_params:
    new_page = query_params["page"]
    if new_page != st.session_state.page:
        st.session_state.page = new_page

# --- Content ---
if st.session_state.page == "home":
    home()

elif st.session_state.page == "addinfo":
    add()

elif st.session_state.page == "scanner":
    webcam()

elif st.session_state.page == "chatbot":
    st.title("💬 Chat Bot")
    user_input = st.text_input("Ask something:")
    if user_input:
        st.write(f"🤖 Bot: You said '{user_input}' — reply coming soon!")

elif st.session_state.page == "add":
    st.markdown("<div class='card'><h3>➕ Add Student</h3></div>", unsafe_allow_html=True)
    with st.form("form_add", clear_on_submit=False):
        name = st.text_input("Full Name")
        roll = st.text_input("Roll Number (unique)")
        dept = st.text_input("Department")
        year = st.text_input("Year / Batch")
        photo = st.file_uploader("Photo (optional)", type=["jpg","jpeg","png"])
        submitted = st.form_submit_button("Save", use_container_width=True)
        if submitted:
            photo_path = None
            if photo:
                ext = Path(photo.name).suffix
                safe_name =f"{roll}.png"
                out = PHOTOS_DIR / safe_name
                with open(out, "wb") as f:
                    f.write(photo.getbuffer())
                photo_path = str(out)
            ok, err = add_student(name, roll, dept, year, photo_path)
            if ok:
                load_known_faces()
                st.success("✅ Student added.")
                st.rerun()
            else:
                st.error(f"❌ Could not add: {err}")

    if st.button("⬅ Back", key="back_button"):
        goto("addinfo")

elif st.session_state.page == "dashboard":
    dashboard()


def icon_class(page):
    return "material-symbols-outlined active" if st.session_state.page == page else "material-symbols-outlined"

home_icon = icon_class("home")
addinfo_icon = icon_class("addinfo")
scanner_icon = icon_class("scanner")
chatbot_icon = icon_class("chatbot")

# --- Navbar ---
st.markdown(f"""
    <div class="bottom-nav">
        <a href="?page=home" title="Home"><span class="{home_icon}">home</span></a>
        <a href="?page=addinfo" title="Add Info"><span class="{addinfo_icon}">note_add</span></a>
        <a href="?page=scanner" title="Scanner"><span class="{scanner_icon}">qr_code_scanner</span></a>
        <a href="?page=chatbot" title="Chat Bot"><span class="{chatbot_icon}">chat_bubble</span></a>
    </div>
""", unsafe_allow_html=True)
