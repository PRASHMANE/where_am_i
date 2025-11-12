import streamlit as st
from PIL import Image
import base64
from add_info import get_student_by_roll
import pandas as pd

CSV_FILE = "deployment/api/Attendance/attendence.csv"
try:
        # Load attendance sheet
    df = pd.read_csv(CSV_FILE)

        # ✅ Normalize column names
    df.columns = df.columns.str.strip().str.title()

        # ✅ Ensure Date column is proper datetime if it exists
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date

except FileNotFoundError:
        st.error(f"❌ File '{CSV_FILE}' not found in current directory")

CSV_FILE1 = "deployment/api/Remark/remark.csv"
try:
        # Load attendance sheet
    df1 = pd.read_csv(CSV_FILE1)

        # ✅ Normalize column names
    df1.columns = df1.columns.str.strip().str.title()

        # ✅ Ensure Date column is proper datetime if it exists
    if 'Date' in df.columns:
        df1['Date'] = pd.to_datetime(df1['Date'], errors='coerce').dt.date

except FileNotFoundError:
        st.error(f"❌ File '{CSV_FILE1}' not found in current directory")




def select1(usn):
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
    st.title("🧾 Student Details")
    col1, col2 = st.columns([1, 2])  # left = image, right = info

    # === LEFT COLUMN (PHOTO) ===
    path=f"data/{usn}.png"
    with col1:
        try:
            # Open the image and read bytes
            with open(path, "rb") as f:
                img_bytes = f.read()
            img_base64 = base64.b64encode(img_bytes).decode()
            
            # Display in glowing div
            st.markdown(f"""
            <div class="image-box">
                <img src="data:image/png;base64,{img_base64}" width="100%" alt="Student Photo">
                <p style="margin-top:10px; color:#00b4d8;">Student Photo</p>
            </div>
            """, unsafe_allow_html=True)
        except FileNotFoundError:
            st.error(f"Image not found at path: {path}")
        
    # === RIGHT COLUMN (DETAILS) ===
    with col2:
        row=get_student_by_roll(usn)
        sid, name1, roll, dept, year, photo_path, updated = row
        #st.subheader("🧾 Student Details")
        name = name1#st.text_input("Full Name")
        roll_no = roll#st.text_input("Roll Number")
        department = dept#st.selectbox("Department", ["CSE", "ECE", "ME", "CE", "EEE"])
        year = year#st.selectbox("Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
        #email = st.text_input("Email")
        #phone = st.text_input("Phone Number")

        st.markdown("<br>", unsafe_allow_html=True)

        #if st.button("Display Information"):
        st.markdown("---")
        st.markdown(f"""
            <div style='background:rgba(0,180,216,0.1); padding:20px; border-radius:15px;'>
            <h3>📋 Student Information Summary</h3>
            <p><b>Name:</b> {name}</p>
            <p><b>Roll Number:</b> {roll_no}</p>
            <p><b>Department:</b> {department}</p>
            <p><b>Year:</b> {year}</p>
            </div>
            """, unsafe_allow_html=True)
        
    st.markdown("---")
    mode = st.radio("Choose View Mode:", ["📊 student Attendance", "🔍 student Remark"], horizontal=True)

    if  mode  ==  "📊 student Attendance":
        # Filter by Student (USN)
            student_list = df['Usn'].unique() if 'Usn' in df.columns else []
            selected_student = st.sidebar.selectbox("Select Student (USN)", options=[usn] + list(student_list))

            # ✅ Filter by Date using a calendar picker (only if Date column exists)
            selected_date = None
            if 'Date' in df.columns:
                selected_date = st.sidebar.date_input("Select Date", value=None)

            # Apply filters
            filtered_df = df.copy()
            if selected_student != "All" and 'Usn' in df.columns:
                filtered_df = filtered_df[filtered_df['Usn'] == selected_student]
            if selected_date and 'Date' in df.columns:
                filtered_df = filtered_df[filtered_df['Date'] == selected_date]

            st.subheader("📋 Student Attendance")
            st.dataframe(filtered_df, use_container_width=True)

            # Summary for filtered data
            if 'Status' in filtered_df.columns and not filtered_df.empty:
                st.subheader("📈 Filtered Attendance Summary")

                total_present = (filtered_df['Status'] == "Present").sum()
                total_absent = (filtered_df['Status'] == "Absent").sum()
                total_classes = total_present + total_absent
                percentage = (total_present / total_classes * 100) if total_classes > 0 else 0

                st.write(f"✅ Present: {total_present}")
                st.write(f"❌ Absent: {total_absent}")
                st.write(f"📊 Attendance Percentage: **{percentage:.2f}%**")
            else:
                st.info("ℹ️ No attendance records match the filter.")

    elif mode == "🔍 student Remark":
            student_list = df1['Usn'].unique() if 'Usn' in df1.columns else []
            selected_student = st.sidebar.selectbox("Select Student (USN)", options=[usn] + list(student_list))

            # ✅ Filter by Date using a calendar picker (only if Date column exists)
            selected_date = None
            if 'Date' in df1.columns:
                selected_date = st.sidebar.date_input("Select Date", value=None)

            # Apply filters
            filtered_df = df1.copy()
            if selected_student != "All" and 'Usn' in df1.columns:
                filtered_df = filtered_df[filtered_df['Usn'] == selected_student]
            if selected_date and 'Date' in df.columns:
                filtered_df = filtered_df[filtered_df['Date'] == selected_date]

            st.subheader("📋 Student Remark")
            st.dataframe(filtered_df, use_container_width=True)
