import streamlit as st
from streamlit_lottie import st_lottie
import requests
import os
import base64

# --- Page setup ---
st.set_page_config(page_title="Where Am I", page_icon="🎓", layout="wide")

# --- Load Lottie Animation ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_ai = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_qp1q7mct.json")

# --- Path to local images ---
image_folder = "image"  # Put your images here
image_files = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith((".png",".jpg",".jpeg"))]

# --- Function to convert image to base64 ---
def img_to_base64(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("utf-8")

# --- Custom CSS ---
st.markdown("""
<style>
body {
    background: linear-gradient(120deg, #0f2027, #203a43, #2c5364);
    color: #fff;
    font-family: 'Poppins', sans-serif;
    overflow-x: hidden;
}
.main-title {
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
    color: #00ffcc;
    text-shadow: 0 0 15px #00ffcc, 0 0 25px #00ffd6;
    margin-top: 40px;
}
.subtitle {
    text-align: center;
    font-size: 1.2rem;
    color: #cfd8dc;
    margin-top: -5px;
}
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

/* ===== SLIDING TAPE ===== */
.slider-container {
    position: relative;
    overflow: hidden;
    width: 100%;
    margin: 50px 0;
}
.slider-track {
    display: flex;
    animation: scroll 20s linear infinite;
}
.slider-track img {
    width: 200px;
    height: 300px;
    margin-right: 15px;
    border-radius: 10px;
    border: 4px solid #00ffcc;
    box-shadow: 0 0 15px #00ffcc;
    object-fit: cover;
}
@keyframes scroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
</style>
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

st.write("")

# --- Prepare HTML for local images ---
if image_files:
    images_html = ""
    for img_path in image_files:
        img_b64 = img_to_base64(img_path)
        images_html += f'<img src="data:image/png;base64,{img_b64}">'
    # Repeat images to make it loop smoothly
    images_html = images_html * 2

    st.markdown(f"""
    <div class="slider-container">
        <div class="slider-track">
            {images_html}
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("No images found in 'images/' folder. Add images first.")

st.write("")

# --- Navigation Button ---
colx, coly, colz = st.columns([1,1,1])
with coly:
    if st.button("🚀 Go to Dashboard"):
        st.switch_page("Dashboard")
