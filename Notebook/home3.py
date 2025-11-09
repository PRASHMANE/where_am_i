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

# Example Lottie: student animation
lottie_ai = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_qp1q7mct.json")

# --- Custom CSS (Refined Student/College Theme) ---
st.markdown("""
<style>
/* ===== BODY & BACKGROUND ===== */
body {
    background: linear-gradient(120deg, #0f2027, #203a43, #2c5364);
    color: #fff;
    font-family: 'Poppins', sans-serif;
    overflow-x: hidden;
}

/* ===== MAIN TITLE ===== */
.main-title {
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
    color: #00ffcc;
    text-shadow: 0 0 15px #00ffcc, 0 0 25px #00ffd6;
    margin-top: 40px;
    animation: slideFade 1.2s ease forwards;
}

.subtitle {
    text-align: center;
    font-size: 1.2rem;
    color: #cfd8dc;
    margin-top: -5px;
    animation: slideFade 1.5s ease forwards;
}

@keyframes slideFade {
    0% {opacity: 0; transform: translateY(-20px);}
    100% {opacity: 1; transform: translateY(0);}
}

/* ===== BUTTON ===== */
.stButton>button {
    background: linear-gradient(135deg, #00ffcc, #00bfa5);
    color: black;
    border-radius: 30px;
    padding: 0.7rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    border: none;
    box-shadow: 0 0 15px #00ffcc, 0 0 30px #00bfa5;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stButton>button:hover {
    transform: scale(1.08);
    box-shadow: 0 0 35px #00ffcc, 0 0 60px #00bfa5;
}

/* ===== FEATURE CARDS ===== */
.feature-card {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 25px;
    text-align: center;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 10px rgba(0, 255, 204, 0.3);
    border: 1px solid rgba(0, 255, 204, 0.3);
    transition: 0.3s ease-in-out;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 25px rgba(0, 255, 204, 0.6);
    border: 1px solid rgba(0, 255, 204, 0.6);
}

/* ===== SOFT ANIMATED LIGHT ACCENTS ===== */
.accent-circle {
    position: absolute;
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: rgba(0, 255, 204, 0.08);
    animation: floatCircle 6s ease-in-out infinite;
    z-index: 0;
}

.accent1 { top: 50px; left: 30px; animation-delay: 0s; }
.accent2 { bottom: 60px; right: 40px; animation-delay: 2s; }
.accent3 { top: 200px; right: 150px; animation-delay: 4s; }

@keyframes floatCircle {
    0%, 100% { transform: translateY(0px) translateX(0px);}
    50% { transform: translateY(-20px) translateX(10px);}
}
</style>

<!-- ===== ACCENT SHAPES ===== -->
<div class="accent-circle accent1"></div>
<div class="accent-circle accent2"></div>
<div class="accent-circle accent3"></div>
""", unsafe_allow_html=True)

# --- Layout ---
st.markdown('<div class="main-title">🎓 Where Am I?</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-based Real-Time Student Location Detection System</div>', unsafe_allow_html=True)
st.write("")
st.write("")

# --- Center Lottie Animation ---
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
        st.switch_page("Dashboard")  # Page title from pages/ folder
