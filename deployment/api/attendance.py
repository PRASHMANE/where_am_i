
def attendance_display():
    import streamlit as st
    import pandas as pd

    st.title("📂 Student Attendance Sheet")

    # CSV file path
    CSV_FILE = "deployment/api/Attendance/attendence.csv"

    try:
        # Load attendance sheet
        df = pd.read_csv(CSV_FILE)

        # ✅ Normalize column names
        df.columns = df.columns.str.strip().str.title()

        # ✅ Ensure Date column is proper datetime if it exists
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date

        # --- Mode Toggle ---
        mode = st.radio("Choose View Mode:", ["📊 Full Attendance", "🔍 Filter Attendance"], horizontal=True)

        if mode == "📊 Full Attendance":
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

        elif mode == "🔍 Filter Attendance":
            st.sidebar.header("🔍 Filters")

            # Filter by Student (USN)
            student_list = df['Usn'].unique() if 'Usn' in df.columns else []
            selected_student = st.sidebar.selectbox("Select Student (USN)", options=["All"] + list(student_list))

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

            st.subheader("📋 Filtered Attendance")
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

    except FileNotFoundError:
        st.error(f"❌ File '{CSV_FILE}' not found in current directory")

