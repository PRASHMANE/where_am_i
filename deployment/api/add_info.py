# add_info.py
import streamlit as st
import sqlite3
from sqlite3 import Connection
from pathlib import Path
import time
from datetime import datetime
import os

# -------------------------
# Config & Setup
# -------------------------
DB_PATH = "students.db"
PHOTOS_DIR = Path("data")
PHOTOS_DIR.mkdir(exist_ok=True)

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
.title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 800;
        color: #00b4d8;
        text-shadow: 0 0 25px #00b4d8;
        margin-top: 40px;
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
# -------------------------
# Database helpers
# -------------------------
def get_conn(path=DB_PATH) -> Connection:
    conn = sqlite3.connect(path, check_same_thread=False)
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll TEXT UNIQUE NOT NULL,
        department TEXT,
        year TEXT,
        photo_path TEXT,
        updated_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def goto(page):
    st.query_params['page'] = page
    st.rerun()

def add_student(name, roll, department, year, photo_path=None):
    conn = get_conn()
    cur = conn.cursor()
    now = datetime.utcnow().isoformat()
    try:
        cur.execute("INSERT INTO students (name, roll, department, year, photo_path, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (name, roll, department, year, photo_path, now))
        conn.commit()
        return True, None
    except sqlite3.IntegrityError as e:
        return False, str(e)
    finally:
        conn.close()

def remove_student(roll):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE roll = ?", (roll,))
    changed = cur.rowcount
    conn.commit()
    conn.close()
    return changed

def update_student(roll, name=None, department=None, year=None, photo_path=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM students WHERE roll = ?", (roll,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return False
    updates = []
    params = []
    if name:
        updates.append("name = ?"); params.append(name)
    if department:
        updates.append("department = ?"); params.append(department)
    if year:
        updates.append("year = ?"); params.append(year)
    if photo_path:
        updates.append("photo_path = ?"); params.append(photo_path)
    if not updates:
        conn.close()
        return False
    params.append(datetime.utcnow().isoformat())
    updates_sql = ", ".join(updates) + ", updated_at = ?"
    params.append(roll)
    cur.execute(f"UPDATE students SET {updates_sql} WHERE roll = ?", params)
    conn.commit()
    conn.close()
    return True

def get_all_students():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, roll, department, year, photo_path, updated_at FROM students ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_student_by_roll(roll):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, roll, department, year, photo_path, updated_at FROM students WHERE roll = ?", (roll,))
    row = cur.fetchone()
    conn.close()
    return row

# -------------------------
# Add Info Page
# -------------------------
def add():
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
    .title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 800;
        color: #00b4d8;
        text-shadow: 0 0 25px #00b4d8;
        margin-top: 40px;
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
    .card-title {
        color: #90e0ef;
        font-weight: 600;
        margin-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
<style>
/* Target Streamlit input labels */
.stTextInput label, .stTextInput div[data-testid="stMarkdownContainer"] p {
    color: #00b4d8 !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    text-shadow: 0 0 15px #00b4d8;
    letter-spacing: 1px;
}

/* Input box styling */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.1);
    color: white;
    border: 1px solid #00b4d8;
    border-radius: 10px;
    padding: 10px 14px;
    transition: 0.3s ease;
}

.stTextInput > div > div > input:focus {
    border-color: #48cae4;
    box-shadow: 0 0 15px #48cae4;
}
</style>
""", unsafe_allow_html=True)
    init_db()  # ensure DB is initialized

    with st.container():
        #st.markdown('<div class="logo"><span style="font-size:26px">🎓</span><div><div style="font-size:18px;font-weight:700">Student Manager</div><div class="small-muted">CRUD • SQLite • Photos • Streamlit</div></div></div>', unsafe_allow_html=True)
        st.markdown('<div class="title">🎓 Student Information Management </div>', unsafe_allow_html=True)
    # Page header
    #st.markdown('<div style="font-size:26px;font-weight:700">🎓 Student Manager</div>', unsafe_allow_html=True)
    #st.markdown('<div class="small-muted">CRUD • SQLite • Photos • Streamlit</div>', unsafe_allow_html=True)
    st.write("---")

    # Navigation buttons
    col1, col2, col3, col4 = st.columns([1,1,1,1])
    with col1:
        if st.button("➕ Add Student"):
            #st.session_state.page = "add"
            st.query_params['page'] = 'add'
    with col2:
        if st.button("🧾 View Students"):
            st.query_params['page'] = 'view'
    with col3:
        if st.button("✏️ Update Student"):
            st.query_params['page'] = "update"
    with col4:
        if st.button("🗑️ Remove Student"):
            st.query_params['page'] = "remove"
    

    st.write("---")
    st.markdown("<div class='card'><h3>Welcome 👋</h3><p class='small-muted'>Use the buttons above to manage students (add, view, update, remove).</p></div>", unsafe_allow_html=True)

    #page = st.session_state.get("page", "add")  # default page inside add_info

    # -------------------------
    # Add Student Page
    # -------------------------
    if st.session_state.page == "add":
  #  st.title("🏠 Home")
 #   st.write("Welcome to the **sky-blue theme** dashboard ✨")

#    if page == "add":
        st.subheader("➕ Add Student")
        with st.form("form_add", clear_on_submit=True):
            name = st.text_input("Full Name")
            roll = st.text_input("Roll Number (unique)")
            dept = st.text_input("Department")
            year = st.text_input("Year / Batch")
            photo = st.file_uploader("Photo (optional)", type=["jpg","jpeg","png"])
            submitted = st.form_submit_button("Save")
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
                    st.success("✅ Student added successfully!")
                else:
                    st.error(f"❌ Could not add student: {err}")

    # -------------------------
    # View Students Page
    # -------------------------
    elif st.session_state.page == "view":
        st.subheader("🧾 All Students")
        search_roll = st.text_input("Search by Roll Number", placeholder="Enter roll number...")
        rows = get_all_students()
        if search_roll:
            rows = [r for r in rows if search_roll.lower() in str(r[2]).lower()]

        if not rows:
            st.info("No students found.")
        else:
            for r in rows:
                sid, name, roll, dept, year, photo_path, updated = r
                cols = st.columns([1,3,1])
                with cols[0]:
                    if photo_path and Path(photo_path).exists():
                        st.image(photo_path, width=80)
                    else:
                        st.image("https://via.placeholder.com/80.png?text=No+Photo")
                with cols[1]:
                    st.markdown(f"**{name}**  \nRoll: {roll}  \nDept: {dept}  \nYear: {year}")
                with cols[2]:
                    if st.button("Select", key=f"select_{sid}"):
                        st.info(f"Selected student: {name}")

    # -------------------------
    # Update Student Page
    # -------------------------
    elif st.session_state.page == "update":
        st.subheader("✏️ Update Student")
        roll_search = st.text_input("Enter Roll Number to update")
        if st.button("Load"):
            rec = get_student_by_roll(roll_search)
            if rec:
                st.session_state.update_rec = rec
            else:
                st.error("Student not found.")

        rec = st.session_state.get("update_rec")
        if rec:
            sid, name, roll, dept, year, photo_path, updated = rec
            with st.form("form_update"):
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
                        st.success("✅ Student updated successfully")
                        st.session_state.pop("update_rec", None)
                    else:
                        st.error("❌ Update failed")

    # -------------------------
    # Remove Student Page
    # -------------------------
    elif st.session_state.page == "remove":
        st.subheader("🗑️ Remove Student")
        roll = st.text_input("Enter Roll Number to remove")
        roll1 = get_student_by_roll(roll)
        print(roll1)
    
        if st.button("Remove"):
            path = f"data/{roll1[2]}.png"
            if os.path.exists(path):
                os.remove(path)
                print("🗑️ Image deleted successfully!")
            else:
                print("⚠️ File not found!")
            changed = remove_student(roll)
            if changed:
                st.success("✅ Student removed.")
            else:
                st.warning("No student found with that roll.")
