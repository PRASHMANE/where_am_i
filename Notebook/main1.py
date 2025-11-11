import streamlit as st

# ============ PAGE CONFIG ============
st.set_page_config(page_title="Where Am I | Cambridge North", layout="wide")

# ============ SESSION STATE ============
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ============ CSS ============ 
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet" />
<style>
body {
    background: radial-gradient(circle at top, #00111a, #000814);
    color: white;
    font-family: 'Poppins', sans-serif;
}

/* CARD */
.card {
    background: rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 2rem;
    margin-top: 2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    transition: transform 0.25s ease;
}
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 6px 30px rgba(0,180,216,0.25);
}

/* BUTTONS */
.stButton>button {
    background: linear-gradient(135deg, #00b4d8, #48cae4);
    color: #fff;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 0.6rem 1.4rem;
    transition: all 0.25s ease-in-out;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 25px rgba(72, 202, 228, 0.6);
}

/* INPUTS */
.stTextInput>div>div>input {
    background: rgba(255,255,255,0.15);
    color: #fff;
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 12px;
    padding: 10px 14px;
}
.stTextInput>div>div>input:focus {
    border-color: #00b4d8;
    box-shadow: 0 0 10px #00b4d8;
}

/* FLOATING NAVBAR */
.navbar {
    position: fixed;
    bottom: 25px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 40, 70, 0.6);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(0,180,216,0.4);
    border-radius: 40px;
    display: flex;
    justify-content: space-around;
    width: 85%;
    max-width: 700px;
    padding: 10px 0;
    box-shadow: 0 0 25px rgba(0,180,216,0.35);
    animation: float 5s ease-in-out infinite alternate;
    z-index: 999;
}
@keyframes float {
    0% { transform: translateX(-50%) translateY(0); }
    50% { transform: translateX(-50%) translateY(-5px); }
    100% { transform: translateX(-50%) translateY(0); }
}

.nav-item {
    text-align: center;
    cursor: pointer;
    transition: transform 0.3s ease, color 0.3s;
    color: #ccc;
}
.nav-item span {
    font-size: 28px;
    display: block;
}
.nav-item:hover {
    transform: scale(1.2);
    color: #fff;
}
.active {
    color: #00b4d8 !important;
    transform: scale(1.3);
}

/* FOOTER */
.footer {
    text-align:center;
    color:#aaa;
    margin-top:3rem;
    font-size:0.85rem;
}
</style>
""", unsafe_allow_html=True)

# ============ NAVBAR ============ 
st.markdown("""
<div class="navbar">
    <form action="" method="get">
        <button name="nav" value="Home" class="nav-item"><span class="material-symbols-outlined">home</span>Home</button>
        <button name="nav" value="Student" class="nav-item"><span class="material-symbols-outlined">school</span>Student</button>
        <button name="nav" value="Camera" class="nav-item"><span class="material-symbols-outlined">photo_camera</span>Camera</button>
        <button name="nav" value="Attendance" class="nav-item"><span class="material-symbols-outlined">fact_check</span>Attendance</button>
    </form>
</div>
""", unsafe_allow_html=True)

# ============ NAVIGATION LOGIC ============
nav_choice = st.query_params.get("nav", [st.session_state.page])[0]
st.session_state.page = nav_choice

# ============ PAGE CONTENT ============
if st.session_state.page == "Home":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## 🏠 Welcome to **Where Am I**")
    st.write("""
    A smart attendance tracking and student monitoring system designed for 
    **Cambridge Institute of Technology – North Campus**.  
    Integrating camera-based detection, student data management, and real-time attendance tracking.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "Student":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## 🎓 Student Details")
    name = st.text_input("Student Name")
    roll = st.text_input("Roll Number")
    dept = st.selectbox("Department", ["CSE", "ECE", "EEE", "MECH", "CIVIL"])
    st.button("Save Student")
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "Camera":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## 📷 Camera / Face Recognition")
    st.write("Use webcam below to capture your face for verification.")
    st.camera_input("Capture Image")
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "Attendance":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## 📑 Attendance Sheet")
    uploaded_file = st.file_uploader("Upload Attendance File (.csv or .xlsx)", type=["csv", "xlsx"])
    if uploaded_file:
        st.success("File uploaded successfully!")
    st.markdown("</div>", unsafe_allow_html=True)

# ============ FOOTER ============
st.markdown("""
<div class="footer">
© 2025 Cambridge Institute of Technology – North Campus | Designed by Prashanth V
</div>
""", unsafe_allow_html=True)
