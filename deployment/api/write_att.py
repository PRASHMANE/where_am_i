import pandas as pd
import os

def write_attendance(usn: str, name: str,att_date, status: str):
    """
    Write a single attendance record to CSV.
    
    Parameters:
        usn (str)    : Student USN
        name (str)   : Student name
        att_date     : Attendance date (datetime.date, datetime, or str)
        status (str) : "Present" or "Absent"
    """
    
    # CSV file path
    CSV_FILE = "deployment/api/Attendance/attendence.csv"

    # Check if file exists
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df.columns = df.columns.str.strip().str.title()
    else:
        # Create new DataFrame if file doesn't exist
        df = pd.DataFrame(columns=["Usn", "Name", "Date", "Status"])

    # Convert date to string (YYYY-MM-DD)
    att_date = pd.to_datetime(att_date).date()

    # Append new record directly
    df.loc[len(df)] = {
        "Usn": usn.strip(),
        "Name": name.strip(),
        "Date": att_date,
        "Status": status.strip().title()  # Normalize "Present"/"Absent"
    }

    # Save to CSV
    df.to_csv(CSV_FILE, index=False)

    print(f"✅ Attendance saved for {name} ({usn}) on {att_date} as {status}")