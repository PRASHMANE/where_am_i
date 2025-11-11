import streamlit as st
import sqlite3
import cv2
import time
from src.models.model import start_webcam,load_known_faces

def webcam():
    # --- Database Setup ---
    def init_db():
        conn = sqlite3.connect("camera_db.db")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cameras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location TEXT NOT NULL,
                url TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def add_camera(name, location, url):
        conn = sqlite3.connect("camera_db.db")
        conn.execute("INSERT INTO cameras (name, location, url) VALUES (?, ?, ?)", (name, location, url))
        conn.commit()
        conn.close()

    def get_cameras():
        conn = sqlite3.connect("camera_db.db")
        rows = conn.execute("SELECT * FROM cameras").fetchall()
        conn.close()
        return rows

    def delete_camera(camera_id):
        conn = sqlite3.connect("camera_db.db")
        conn.execute("DELETE FROM cameras WHERE id=?", (camera_id,))
        conn.commit()
        conn.close()

    # --- Initialize database ---
    init_db()

    # --- Streamlit UI Setup ---
    #st.set_page_config(page_title="Camera Manager", layout="wide")
    st.title("🎥 Camera Management Dashboard")
    st.markdown("Manage your camera URLs and view live streams instantly!")

    menu = ["Add Camera", "View Cameras", "Live View"]
    choice = st.sidebar.radio("📋 Menu", menu)

    # --- Add Camera Page ---
    if choice == "Add Camera":
        st.subheader("➕ Add a New Camera")

        name = st.text_input("Camera Name")
        location = st.text_input("Location Name")
        url = st.text_input("Camera Stream URL (RTSP or IP URL)")

        if st.button("💾 Save Camera"):
            if name and location and url:
                add_camera(name, location, url)
                st.success(f"✅ Camera '{name}' added successfully!")
            else:
                st.warning("⚠️ Please fill all fields before saving.")

    # --- View Cameras Page ---
    elif choice == "View Cameras":
        st.subheader("📋 Saved Cameras")
        cameras = get_cameras()

        if not cameras:
            st.info("No cameras saved yet.")
        else:
            for cam in cameras:
                col1, col2, col3, col4 = st.columns([2, 2, 3, 1])
                with col1:
                    st.write(f"**📸 Name:** {cam[1]}")
                with col2:
                    st.write(f"📍 **Location:** {cam[2]}")
                with col3:
                    st.code(cam[3], language="text")
                with col4:
                    if st.button("🗑️ Delete", key=f"del_{cam[0]}"):
                        delete_camera(cam[0])
                        st.rerun()

    # --- Live View Page ---
    elif choice == "Live View":
        st.subheader("🎦 Live Camera Feeds")
        cameras = get_cameras()
        #load_known_faces()
        start_webcam(cameras)
