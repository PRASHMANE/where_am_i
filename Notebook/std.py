import streamlit as st
from PIL import Image

# === PAGE CONFIG ===
st.set_page_config(page_title="Student Info", layout="wide")

# === CUSTOM CSS (Dark + Blue Theme) ===
st.markdown("""
<style>
body {
    background-color: #0a0a1a;
    color: #ffffff;
}
h1, h2, h3, h4, h5, h6 {
    color: #00b4d8;
    text-shadow: 0 0 15px #00b4d8;
}
div[data-testid="stSidebar"] {
    background-color: #0a0a1a;
}
div[data-testid="column"] {
    background: rgba(10, 10, 26, 0.8);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 0 20px rgba(0, 180, 216, 0.3);
}
input, select, textarea {
    background-color: #1b1b2f !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    border: 1px solid #00b4d8 !important;
}
.stButton button {
    background-color: #00b4d8;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: bold;
    box-shadow: 0 0 15px #00b4d8;
}
.stButton button:hover {
    background-color: #0096c7;
    box-shadow: 0 0 25px #00b4d8;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.image-box {
    background-color: rgba(10, 10, 26, 0.6);
    border-radius: 20px;
    padding: 15px;
    box-shadow: 0 0 30px rgba(0, 180, 216, 0.6);
    text-align: center;
    margin-top: 10px;
}
.image-box img {
    border-radius: 15px;
    box-shadow: 0 0 25px rgba(0, 180, 216, 0.5);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="image-box">
    <img src="https://via.placeholder.com/200" width="100%" alt="Student Photo">
</div>
""", unsafe_allow_html=True)


# === PAGE TITLE ===
st.markdown("<h1 style='text-align:center;'>🎓 Student Information</h1>", unsafe_allow_html=True)

# === LAYOUT ===
col1, col2 = st.columns([1, 2])  # left = image, right = info

# === LEFT COLUMN (IMAGE) ===
with col1:
    st.subheader("📸 Student Photo")
    uploaded_file = st.file_uploader("Upload Student Image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Student Photo", use_container_width=True)
    else:
        st.info("Please upload a student photo.")

# === RIGHT COLUMN (INFO) ===
with col2:
    st.subheader("🧾 Student Details")
    name = st.text_input("Full Name")
    roll_no = st.text_input("Roll Number")
    department = st.selectbox("Department", ["CSE", "ECE", "ME", "CE", "EEE"])
    year = st.selectbox("Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Display Information"):
        st.markdown("---")
        st.markdown(f"""
        <div style='background:rgba(0,180,216,0.1); padding:20px; border-radius:15px;'>
        <h3>📋 Student Information Summary</h3>
        <p><b>Name:</b> {name}</p>
        <p><b>Roll Number:</b> {roll_no}</p>
        <p><b>Department:</b> {department}</p>
        <p><b>Year:</b> {year}</p>
        <p><b>Email:</b> {email}</p>
        <p><b>Phone:</b> {phone}</p>
        </div>
        """, unsafe_allow_html=True)
