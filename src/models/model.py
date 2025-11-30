import streamlit as st
import cv2
import numpy as np
from insightface.app import FaceAnalysis
import os
from PIL import Image
import time
from deployment.api.add_info import get_student_by_roll 
from datetime import datetime
from deployment.api.write_att import write_attendance
from deployment.api.write_remark import write_remark
from src.models.f import filter_img

# =====================
# PAGE CONFIG
# =====================
#st.set_page_config(page_title="Face Recognition | Where Am I", layout="wide")
#st.title("🎥 Real-Time Face Recognition (CPU)")
#st.markdown("This app uses **RetinaFace + ArcFace** to identify faces from your webcam feed.")

# =====================
# FACE ANALYSIS MODEL
# =====================
@st.cache_resource
def load_face_model():
    app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
    app.prepare(ctx_id=-1, det_size=(640, 640))
    return app

app = load_face_model()
track=[]
track1=[]


# =====================
# LOAD KNOWN FACES
# =====================
known_faces = {}
known_embeddings = []
def load_known_faces(known_dir="data"):
    if not os.path.exists(known_dir):
        st.warning(f"⚠️ Folder '{known_dir}' not found!")
        return known_faces, known_embeddings

    for file in os.listdir(known_dir):
        if file.lower().endswith(('.jpg', '.png', '.jpeg')):
            name = os.path.splitext(file)[0]
            img_path = os.path.join(known_dir, file)
            img = cv2.imread(img_path)
            faces = app.get(img)
            if len(faces) > 0:
                emb = faces[0].normed_embedding
                known_faces[name] = emb
                known_embeddings.append((name, emb))
                print("✅ Loaded face ")
            else:
                #st.warning(f"No face found in {file}")
                pass
    #return known_faces, known_embeddings
    #print("✅ Loaded face ")
#known_faces, known_embeddings = load_known_faces()
load_known_faces()
# =====================
# UTILITY FUNCTION
# =====================
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# =====================
# START WEBCAM
# =====================
def start_webcam(cameras):
    place=["libraray","coridor","ground","canteen"]
    if not cameras:
            st.info("No cameras available. Please add one first.")
    else:
         
        if "camera_states" not in st.session_state:
            st.session_state.camera_states = {}

        for cam in cameras:
            cam_id, cam_name, cam_location, cam_url = cam
            st.markdown(f"### 📍 {cam_name} — {cam_location}")

            if cam_id not in st.session_state.camera_states:
                st.session_state.camera_states[cam_id] = False


            # Toggle button
            toggle_label = "🟢 Stop Feed" if st.session_state.camera_states[cam_id] else "▶️ Start Feed"
            if st.button(toggle_label, key=f"toggle_{cam_id}"):
                st.session_state.camera_states[cam_id] = not st.session_state.camera_states[cam_id]
                st.rerun()

            if st.session_state.camera_states[cam_id]:
                st.info(f"Streaming live from **{cam_name}**...")

                cap = cv2.VideoCapture(cam_url)
                stframe = st.empty()


                if not cap.isOpened():
                    st.error("❌ Could not open stream. Please check the URL.")
                    st.session_state.camera_states[cam_id] = False
                    continue

                start_time = time.time()

                while st.session_state.camera_states[cam_id]:
                    ret, frame = cap.read()
                    if not ret:
                        st.error("⚠️ Stream ended or not reachable.")
                        break
                    frame=filter_img(frame)
                    faces = app.get(frame)

                    for face in faces:
                        bbox = face.bbox.astype(int)
                        x1, y1, x2, y2 = bbox
                        emb = face.normed_embedding
                        best_match = None
                        best_score = 0.0

                        for name, known_emb in known_embeddings:
                            score = cosine_similarity(emb, known_emb)
                            if score > best_score:
                                best_score = score
                                best_match = name

                        #label = best_match if best_score > 0.60 else "Unknown"
                        #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        #cv2.putText(frame, f"{label} ({best_score:.2f})", (x1, y1 - 10),
                         #       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                        if best_score > 0.60 :
                            label = best_match
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            cv2.putText(frame, f"{label} ({best_score:.2f})", (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 255, 0), 3)
                            
                            if label not in track and cam_location not in place:
                                row=get_student_by_roll(label)
                                track.append(label)
                                if row:
                                    sid, name1, roll, dept, year, photo_path, updated = row
                                    write_attendance(roll, name1, datetime.now(), "Present")
                                else:
                                    print("❌ No student record found for this roll.")

                            elif label not in track and  cam_location in place:
                                row=get_student_by_roll(label)
                                track1.append(label)
                                if row:
                                    sid, name1, roll, dept, year, photo_path, updated = row
                                    write_remark(roll, name1, datetime.now(),cam_location)




                        else:
                            label = "Unknown"
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0,255), 2)
                            cv2.putText(frame, label, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 0, 255), 3)


                        #if label not in track and cam_location not in place: 
                         #   row=get_student_by_roll(label)
                          #  track.append(label)
                           # if row:
                            #    sid, name1, roll, dept, year, photo_path, updated = row
                             #   write_attendance(roll, name1, datetime.now(), "Present")
                           # else:
                            #    print("❌ No student record found for this roll.")
                        #write_attendance(row[1],row[0],datetime.now(),"Present")
                       # elif label not in track and  cam_location in place:
                        #    row=get_student_by_roll(label)
                         #   track1.append(label)
                          #  if row:
                           #     sid, name1, roll, dept, year, photo_path, updated = row
                            #    write_remark(roll, name1, datetime.now(),cam_location)


                    cv2.putText(frame, f"Faces: {len(faces)}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    stframe.image(frame, channels="RGB", use_container_width=True)

                    time.sleep(0.03)

                    if time.time() - start_time > 300:
                        st.warning("⏹ Auto-stopped after 5 minutes to save resources.")
                        st.session_state.camera_states[cam_id] = False
                        break
                
                cap.release()
                st.rerun()
            

    

    

    
    



        