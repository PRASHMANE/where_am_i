import streamlit as st
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

def attendance_display():
    import streamlit as st
    st.markdown("""
    <style>
    /* Page background and text */
    body {
        background-color: #0a0a1a;
        color: #ffffff;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #00b4d8;
        text-shadow: 0 0 15px #00b4d8;
    }

    /* Sidebar background */
    div[data-testid="stSidebar"] {
        background-color: #0a0a1a;
        color: #ffffff;
    }

    /* DataFrame table styling */
    div[data-testid="stDataFrame"] {
        background-color: rgba(10, 10, 26, 0.9);
        color: #ffffff;
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 0 15px rgba(0,180,216,0.4);
    }

    /* Table headers */
    div[data-testid="stDataFrame"] thead tr th {
        background-color: #0a0a1a !important;
        color: #00b4d8 !important;
    }

    /* Table rows */
    div[data-testid="stDataFrame"] tbody tr td {
        color: #ffffff !important;
    }

    /* Radio buttons (mode toggle) */
    div[data-baseweb="radio"] label {
        color: #00b4d8 !important;
    }

    /* Sidebar selectboxes and date input */
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
    </style>
    """, unsafe_allow_html=True)

    import streamlit as st
    import pandas as pd

    st.title("📂 Student Attendance Sheet & Risk Sheet")

    # CSV file path
    #CSV_FILE = "deployment/api/Attendance/attendence.csv"

    #try:
        # Load attendance sheet
     #   df = pd.read_csv(CSV_FILE)

        # ✅ Normalize column names
      #  df.columns = df.columns.str.strip().str.title()

    # ✅ Ensure Date column is proper datetime if it exists
       # if 'Date' in df.columns:
          #  df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date

        # --- Mode Toggle ---
    mode = st.radio("Choose View Mode:", ["📊 student Attendance", "🔍 Student Risk"], horizontal=True)

    if mode == "📊 student Attendance":
            # Show entire attendance sheet
            st.subheader("📊 Full Attendance Table")
            st.dataframe(df, use_container_width=True)

            # Summary
            if 'Status' in df.columns:
                st.subheader("📈 Attendance Summary")
                total_present = (df['Status'] == "Present").sum()
                total_absent = (df['Status'] == "Absent").sum()
                total_classes = total_present + total_absent
                percentage = (total_present / total_classes * 100) if total_classes > 0 else 0

                st.write(f"✅ Total Present: {total_present}")
                st.write(f"❌ Total Absent: {total_absent}")
                st.write(f"📊 Overall Attendance: **{percentage:.2f}%**")

    elif mode == "🔍 Student Risk":
            st.subheader("📊 Student Risk Table")
            st.dataframe(df1, use_container_width=True)
