import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
import base64

def dashboard():
    # === CUSTOM CSS ===
    st.markdown("""
    <style>
    body {
        background: radial-gradient(circle at top, #0a0a0a, #1a1a1a, #000000);
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
    }

    h1, h2, h3 {
        color: #00ffc3;
        text-shadow: 0 0 10px #00ffc3;
    }

    .card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 20px rgba(0,255,204,0.3);
        border: 1px solid rgba(0,255,204,0.2);
    }

    .image-frame {
        border: 3px solid #45a29e;
        border-radius: 15px;
        box-shadow: 0 0 25px rgba(102, 252, 241, 0.6);
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
    }

    .image-frame:hover {
        transform: scale(1.03);
        box-shadow: 0 0 40px rgba(102, 252, 241, 1);
    }

    .caption {
        text-align: center;
        color: #66fcf1;
        font-weight: 600;
        margin-top: 5px;
        font-size: 1.1rem;
    }

    [data-testid="stPlotlyChart"] {
        background: rgba(0,0,0,0.5);
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 0 20px rgba(0,255,204,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    # === HEADER ===
    st.markdown("<h1 style='text-align:center;'>📊 Where Am I — Smart Vision Dashboard</h1>", unsafe_allow_html=True)
    st.write("### Phase 1: Comparing **face_recognition** vs **RetinaFace** on accuracy, speed, and frame detection quality.")

    # === PHASE 1 ===
    data = {
        "Model": ["face_recognition", "RetinaFace"],
        "Accuracy (%)": [75.2, 97.6],
        "Avg Detection Time (ms)": [230, 85],
        "Multi-face Handling (Faces/frame)": [10, 50]
    }
    df = pd.DataFrame(data)
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown("<div class='card'><h3>🔍 Performance Comparison</h3></div>", unsafe_allow_html=True)
        chart = px.bar(
            df.melt(id_vars="Model", var_name="Metric", value_name="Value"),
            x="Metric", y="Value", color="Model", barmode="group", text_auto=True,
            color_discrete_sequence=["#00ffcc", "#ff4d6d"]
        )
        st.plotly_chart(chart, use_container_width=True)

    with col2:
        st.markdown("<div class='card'><h3>📷 Frame Comparison</h3></div>", unsafe_allow_html=True)
        img1 = Image.open("/Users/prashmane/Documents/where_am_i/data/data1/face_recgnition1.jpg")
        st.image(img1, use_container_width=True)
        st.markdown("<div class='caption'>Face Recognition Output</div>", unsafe_allow_html=True)
        img2 = Image.open("/Users/prashmane/Documents/where_am_i/data/data1/retinaface1.jpg")
        st.image(img2, use_container_width=True)
        st.markdown("<div class='caption'>RetinaFace Output</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><h3>🧠 Summary of Phase 1</h3></div>", unsafe_allow_html=True)
    st.markdown("""
    - ✅ **RetinaFace** provides much higher detection accuracy and handles multiple faces simultaneously.  
    - ⚡ Detection speed is ~3× faster on average.  
    - 📸 Suitable for real-time classroom tracking.  
    - 🧩 Next: add pre-filtering and feature fusion for higher precision.
    """)
    st.markdown("---")

    # === PHASE 2 ===
    st.markdown("<div class='card'><h3>🎨 Phase 2: RGB Filter — Accuracy & Face Count Impact</h3></div>", unsafe_allow_html=True)
    col3, col4 = st.columns([1, 1])
    with col3:
        img_before = Image.open("/Users/prashmane/Documents/where_am_i/data/data1/face_count1.jpg")
        st.image(img_before, use_container_width=True)
        st.markdown("<div class='caption'>Before RGB Filter</div>", unsafe_allow_html=True)
    with col4:
        img_after = Image.open("/Users/prashmane/Documents/where_am_i/data/data1/face_count.jpg")
        st.image(img_after, use_container_width=True)
        st.markdown("<div class='caption'>After RGB Filter</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><h3>📈 Accuracy and Face Count Comparison</h3></div>", unsafe_allow_html=True)
    df_phase2 = pd.DataFrame({
        "Condition": ["Before RGB Filter", "After RGB Filter"],
        "Accuracy (%)": [88.4, 96.8],
        "Detected Faces": [349, 357]
    })
    fig_phase2 = px.bar(
        df_phase2, x="Condition", y="Detected Faces", text_auto=True,
        color="Condition", color_discrete_sequence=["#ff4d6d", "#00ffcc"]
    )
    fig_phase2.add_scatter(
        x=df_phase2["Condition"], y=df_phase2["Accuracy (%)"], mode="lines+markers+text",
        name="Accuracy (%)", text=df_phase2["Accuracy (%)"].astype(str) + "%",
        textposition="top center", line=dict(color="#00bfff", width=3), marker=dict(size=10)
    )
    fig_phase2.update_layout(
        plot_bgcolor="rgba(0,0,0,0.5)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff", size=14), title_font=dict(size=20, color="#00ffc3")
    )
    st.plotly_chart(fig_phase2, use_container_width=True)
    st.markdown("""
    - 🎯 Accuracy increased **88.4 → 96.8 %** after RGB filtering.  
    - 👥 Face count improved **349 → 357** due to better contrast.  
    - 🌈 RGB filter enhances visibility and precision.  
    """)
    st.markdown("---")

    # === PHASE 3: RetinaFace + ArcFace Integration ===
    st.markdown("<div class='card'><h3>🤖 Phase 3: RetinaFace + ArcFace Integration</h3></div>", unsafe_allow_html=True)
    st.write("In this phase, RetinaFace (detection) and ArcFace (recognition) are combined into a real-time AI pipeline.")

    try:
        arch_img = Image.open("/Users/prashmane/Documents/where_am_i/data/data1/phase3_architecture.png")
        st.image(arch_img, caption="RetinaFace + ArcFace System Architecture", use_container_width=True)
    except:
        st.info("Add an architecture diagram at `/data/data1/phase3_architecture.png` to display it here.")

    df_phase3 = pd.DataFrame({
        "Metric": ["Detection Accuracy (%)", "Recognition Accuracy (%)", "Avg FPS", "Faces per Frame"],
        "Before Integration": [97.6, 0, 15, 50],
        "After Integration": [97.6, 94.8, 12, 50]
    })
    chart3 = px.bar(
        df_phase3.melt(id_vars="Metric", var_name="Phase", value_name="Value"),
        x="Metric", y="Value", color="Phase", barmode="group", text_auto=True,
        color_discrete_sequence=["#00bfa5", "#ff4d6d"]
    )
    st.plotly_chart(chart3, use_container_width=True)

    st.markdown("""
    ### 🧠 Phase 3 Summary
    - ✅ **RetinaFace** precisely detects and aligns faces.  
    - 🧬 **ArcFace** extracts embeddings and matches them with database entries.  
    - ⚙️ Combined system achieves **94–98 % end-to-end recognition accuracy**.  
    - 📡 Operates in real time (~12 FPS on CPU, higher on GPU).  
    - 🎓 Enables **student identity recognition and attendance mapping** from live camera feeds.  
    """)
    st.markdown("---")

    st.markdown("<br><center><small>© 2025 Where Am I | AI-Based Student Tracking</small></center>", unsafe_allow_html=True)
