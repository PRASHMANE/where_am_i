import streamlit as st
from add_info import add_info,add_student,get_all_students,get_student_by_roll,goto,update_student,remove_student
from cam import webcam
from pathlib import Path
import streamlit as st
import sqlite3
from sqlite3 import Connection
from datetime import datetime
import time
from home import home

DB_PATH = "students.db"
PHOTOS_DIR = Path("data")
PHOTOS_DIR.mkdir(exist_ok=True)
# --- Page setup ---
st.set_page_config(page_title="Sky Blue Theme App", layout="wide")

# --- Load Material Icons ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined"
          rel="stylesheet" />
""", unsafe_allow_html=True)

# --- Sky Blue Theme CSS ---
st.markdown("""
    <style>
    /* === Full Screen Sky Blue Background === */
    html, body, [class*="stApp"], .main, .block-container {
        background-color: #87ceeb !important; /* sky blue */
        color: #0a0a0a !important; /* dark text for readability */
    }

    /* Widget styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > input {
        background-color: #b0e0e6 !important; /* lighter sky blue for inputs */
        color: #0a0a0a !important;
        border: 1px solid #1e90ff !important;
        border-radius: 10px !important;
        padding: 0.5rem 0.75rem !important;
    }

    .stButton>button {
        background: #1e90ff !important; /* dodger blue button */
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        transition: 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background: #00bfff !important; /* deep sky blue on hover */
        transform: scale(1.05);
        box-shadow: 0 0 15px #00bfff;
    }

    /* Bottom Navigation */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #87ceeb; /* solid sky blue */
        border-top: 1px solid #1e90ff;
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 14px 0;
        z-index: 100;
    }

    .material-symbols-outlined {
        font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 48;
        font-size: 30px;
        color: #0a0a0a;
        cursor: pointer;
        transition: all 0.3s ease-in-out;
        padding: 8px;
        border-radius: 50%;
    }
    .material-symbols-outlined:hover {
        color: #ffffff;
        transform: scale(1.2);
        text-shadow: 0 0 12px #1e90ff;
        background: rgba(30,144,255,0.3);
    }
    .active {
        color: #ffffff !important;
        text-shadow: 0 0 16px #1e90ff;
        background: rgba(30,144,255,0.3);
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
  background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(0,0,0,0.02));
  border-radius: 12px;
  padding: 18px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.25);
  transition: transform .18s ease, box-shadow .18s ease;
}
.card:hover { transform: translateY(-6px); box-shadow: 0 12px 30px rgba(0,0,0,0.35); }
.btn-glow {
  border-radius: 10px;
  padding: 10px 14px;
  font-weight:600;
  box-shadow: 0 6px 20px rgba(0,150,255,0.12);
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
    #st.title("🏠 Home")
    #st.write("Welcome to the **sky-blue theme** dashboard ✨")
    home()

elif st.session_state.page == "addinfo":
    add_info()

elif st.session_state.page == "scanner":
    webcam()

elif st.session_state.page == "chatbot":
    st.title("💬 Chat Bot")
    user_input = st.text_input("Ask something:")
    if user_input:
        st.write(f"🤖 Bot: You said '{user_input}' — reply coming soon!")

elif st.session_state.page == "add":
    #st.title("➕ Add Student")
    #st.write("This is the Add Student page.")
    #def goto(page):
     #   st.query_params['page'] = page
      #  st.rerun()
    st.markdown("<div class='card'><h3>➕ Add Student</h3></div>", unsafe_allow_html=True)
    st.markdown("\n")
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
                safe_name = f"{roll}_{int(time.time())}{ext}"
                out = PHOTOS_DIR / safe_name
                with open(out, "wb") as f:
                    f.write(photo.getbuffer())
                photo_path = str(out)
            ok, err = add_student(name, roll, dept, year, photo_path)
            if ok:
                st.success("✅ Student added.")
                st.rerun()
            else:
                st.error(f"❌ Could not add: {err}")

    if st.button("⬅ Back"):
        goto("addinfo")

elif st.session_state.page == "view":
    st.markdown("<div class='card'><h3>🧾 All Students</h3></div>", unsafe_allow_html=True)
    st.markdown("\n")

    # 🔍 Search bar + button in one row
    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        search_roll = st.text_input("Search by Roll Number", placeholder="Enter roll number...")
    with search_col2:
        st.markdown("\n")
        st.markdown("\n")
        search_clicked = st.button("🔍 Search")

    # Get all students from DB
    rows = get_all_students()
    if not rows:
        st.info("No students in the database yet.")
    else:
        # Filter only when search button clicked and input not empty
        if search_clicked and search_roll:
            rows = [r for r in rows if search_roll.lower() in str(r[2]).lower()]  # r[2] = roll

            if not rows:
                st.warning("No matching student found.")

        # Display all (or filtered) students
        for r in rows:
            sid, name, roll, dept, year, photo_path, updated = r
            cols = st.columns([1, 4, 1])
            with cols[0]:
                st.markdown("\n")
                if photo_path and Path(photo_path).exists():
                    st.image(photo_path, width=90)
                else:
                    st.image("https://via.placeholder.com/90x90.png?text=No+Photo", width=50)
            with cols[1]:
                st.markdown("\n")
                st.markdown(f"**{name}**  \n**Roll:** {roll}  \n**Dept:** {dept}  \n**Year:** {year}")
                st.markdown(f"<div class='small-muted'>Updated: {updated or '—'}</div>", unsafe_allow_html=True)
            with cols[2]:
                st.markdown("\n")
                if st.button("Select", key=f"select_{sid}"):
                    st.session_state.page = "home"
                    st.rerun()
            st.write("---")

    if st.button("⬅ Back"):
        goto("addinfo")

elif st.session_state.page == "update":
    st.markdown("<div class='card'><h3>✏️ Update Student</h3></div>", unsafe_allow_html=True)
    st.markdown("\n")
    roll_search = st.text_input("Enter Roll Number to update", key="upd_roll_search")
    if st.button("Load"):
        rec = get_student_by_roll(roll_search)
        if not rec:
            st.error("Student not found.")
        else:
            st.session_state.update_rec = rec
            st.rerun()

    rec = st.session_state.get("update_rec", None)
    if rec:
        sid, name, roll, dept, year, photo_path, updated = rec
        with st.form("form_upd"):
            name_n = st.text_input("Full Name", value=name)
            dept_n = st.text_input("Department", value=dept)
            year_n = st.text_input("Year / Batch", value=year)
            photo = st.file_uploader("Replace Photo (optional)", type=["jpg","jpeg","png"])
            sub = st.form_submit_button("Update")
            if sub:
                photo_path_new = None
                if photo:
                    ext = Path(photo.name).suffix
                    safe_name = f"{roll}_{int(time.time())}{ext}"
                    out = PHOTOS_DIR / safe_name
                    with open(out, "wb") as f:
                        f.write(photo.getbuffer())
                    photo_path_new = str(out)
                ok = update_student(roll, name_n, dept_n, year_n, photo_path_new)
                if ok:
                    st.success("✅ Updated successfully")
                    st.session_state.pop("update_rec", None)
                    st.rerun()
                else:
                    st.error("❌ Update failed")
    if st.button("⬅ Back"):
        goto("addinfo")

elif st.session_state.page == "remove":
    st.markdown("<div class='card'><h3>🗑️ Remove Student</h3></div>", unsafe_allow_html=True)
    st.markdown("\n")
    roll = st.text_input("Enter Roll Number to remove", key="rm_roll")
    if st.button("Remove"):
        changed = remove_student(roll)
        if changed:
            st.success("✅ Student removed.")
        else:
            st.warning("No student found with that roll.")
    if st.button("⬅ Back"):
        goto("addinfo")


# --- Active icon handler ---
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
