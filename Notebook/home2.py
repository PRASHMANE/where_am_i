import streamlit as st
from streamlit_lottie import st_lottie
import requests

# --- Page setup ---
st.set_page_config(page_title="Where Am I", page_icon="🎓", layout="wide")

# --- Load Lottie Animation ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Example Lottie: student with laptop
lottie_ai = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_qp1q7mct.json")

# --- Custom CSS (student/college themed) ---
st.markdown("""
<style>
/* ===== BACKGROUND ===== */
body {
    background: radial-gradient(circle at top left, #0b0c10, #1f2833, #0b0c10);
    color: #fff;
    font-family: 'Poppins', sans-serif;
    overflow-x: hidden;
}

/* ===== TITLE ANIMATION ===== */
@keyframes fadeInSlide {
    0% {opacity: 0; transform: translateY(-30px);}
    100% {opacity: 1; transform: translateY(0);}
}

.main-title {
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
    animation: fadeInSlide 1.2s ease-in-out;
    color: #66fcf1;
    text-shadow: 0 0 25px #45a29e, 0 0 50px #45a29e;
    margin-top: 40px;
}

.subtitle {
    text-align: center;
    color: #c5c6c7;
    font-size: 1.2rem;
    margin-top: -10px;
    animation: fadeInSlide 1.5s ease-in-out;
}

/* ===== BUTTON STYLE ===== */
.stButton>button {
    background: linear-gradient(90deg, #45a29e, #66fcf1);
    color: black;
    border-radius: 25px;
    padding: 0.75rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    border: none;
    box-shadow: 0 0 20px #45a29e, 0 0 40px #66fcf1;
    transition: all 0.3s ease-in-out;
}

.stButton>button:hover {
    transform: scale(1.08);
    box-shadow: 0 0 35px #66fcf1, 0 0 60px #45a29e;
}

/* ===== FEATURE CARDS ===== */
.feature-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 25px;
    text-align: center;
    backdrop-filter: blur(12px);
    box-shadow: 0 0 15px rgba(102, 252, 241, 0.3);
    transition: 0.3s ease-in-out;
    border: 1px solid rgba(102, 252, 241, 0.3);
}

.feature-card:hover {
    transform: translateY(-7px) scale(1.02);
    box-shadow: 0 0 30px rgba(102, 252, 241, 0.6), 0 0 60px rgba(102, 252, 241, 0.4);
    border: 1px solid rgba(102, 252, 241, 0.6);
}

/* ===== FLOATING STUDENT/COLLEGE SHAPES ===== */
.student-shape {
    position: absolute;
    width: 120px;
    height: 120px;
    background: url('https://cdn-icons-png.flaticon.com/512/3135/3135715.png') no-repeat center;
    background-size: contain;
    animation: float 6s ease-in-out infinite;
    opacity: 0.15;
    z-index: 0;
}

.cap-shape {
    position: absolute;
    width: 100px;
    height: 100px;
    background: url('https://cdn-icons-png.flaticon.com/512/3135/3135710.png') no-repeat center;
    background-size: contain;
    animation: float 8s ease-in-out infinite;
    opacity: 0.15;
    z-index: 0;
}

.student1 { top: 30px; left: 20px; animation-delay: 0s; }
.student2 { bottom: 60px; right: 40px; animation-delay: 3s; }
.cap1 { top: 150px; right: 100px; animation-delay: 1s; }

@keyframes float {
    0%, 100% { transform: translateY(0px) translateX(0px); }
    50% { transform: translateY(-25px) translateX(15px); }
}
</style>

<!-- ===== FLOATING SHAPES ===== -->
<div class="student-shape student1"></div>
<div class="student-shape student2"></div>
<div class="cap-shape cap1"></div>
""", unsafe_allow_html=True)

# --- Layout ---
st.markdown('<div class="main-title">🎓 Where Am I?</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-based Real-Time Student Location Detection System</div>', unsafe_allow_html=True)
st.write("")
st.write("")

# --- Center Animation ---
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if lottie_ai:
        st_lottie(lottie_ai, height=300, key="ai")
    else:
        st.warning("Animation failed to load.")

# --- Feature Cards ---
st.write("### 🚀 Features")
colA, colB, colC = st.columns(3)
with colA:
    st.markdown("""
    <div class="feature-card">
        <h4>Face Recognition</h4>
        <p>Detect and identify students in real-time using ArcFace + RetinaFace.</p>
    </div>
    """, unsafe_allow_html=True)
with colB:
    st.markdown("""
    <div class="feature-card">
        <h4>Smart Zone Mapping</h4>
        <p>Automatically determine if a student is in class, library, or canteen.</p>
    </div>
    """, unsafe_allow_html=True)
with colC:
    st.markdown("""
    <div class="feature-card">
        <h4>Live Analytics</h4>
        <p>View attendance insights and movement patterns in a clean dashboard.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# --- Navigation Button ---
colx, coly, colz = st.columns([1,1,1])
with coly:
    if st.button("🚀 Go to Dashboard"):
        st.switch_page("Dashboard")
