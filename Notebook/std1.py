import streamlit as st
from PIL import Image
import base64

# === PAGE CONFIG ===
st.set_page_config(page_title="Student Info", layout="wide")

# === CUSTOM CSS (Dark + Blue Theme + Photo Shadow) ===
st.markdown("""
<style>
body {
    background-color: #0a0a1a;
    color: #ffffff;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    color: #00b4d8;
    text-shadow: 0 0 15px #00b4d8;
}

/* Column container */
div[data-testid="column"] {
    background: rgba(10, 10, 26, 0.8);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 0 20px rgba(0, 180, 216, 0.3);
}

/* Input boxes */
input, select, textarea {
    background-color: #1b1b2f !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    border: 1px solid #00b4d8 !important;
}

/* Buttons */
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

/* Image container with glow */
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

# === TITLE ===
st.markdown("<h1 style='text-align:center;'>🎓 Student Information</h1>", unsafe_allow_html=True)

# === LAYOUT ===
col1, col2 = st.columns([1, 2])  # left = image, right = info

# === LEFT COLUMN (PHOTO) ===
with col1:
    st.subheader("📸 Student Photo")
    uploaded_file = st.file_uploader("Upload Student Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
    # Open the image with PIL
        img = Image.open(uploaded_file)
        
        # Convert to base64 for embedding
        uploaded_file.seek(0)  # reset file pointer to the start
        img_bytes = uploaded_file.read()
        img_base64 = base64.b64encode(img_bytes).decode()
        
        st.markdown(f"""
        <div class="image-box">
            <img src="data:image/png;base64,{img_base64}" width="100%" alt="Student Photo">
            <p style="margin-top:10px; color:#00b4d8;">Uploaded Student Photo</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Please upload a student photo.")

# === RIGHT COLUMN (DETAILS) ===
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
