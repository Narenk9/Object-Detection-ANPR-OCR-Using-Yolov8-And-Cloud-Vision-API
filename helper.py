# packages
import streamlit as st
from moviepy.editor import VideoFileClip
from io import BytesIO
import tempfile
import numpy as np
import cv2
from ultralytics import YOLO
from PIL import Image
import time
import os
@st.cache_resource
def load_model(model_path):
    """
    Loads a YOLO object detection model from 
    specified model_path
    Parameters:
        model_path (str): The path to the YOLO model file.

    Returns:
        A YOLO object detection model
    """
    model = YOLO(model_path)
    return model

def display_detected_frames(model,st_frame,image):
    # Predict objects in image
    res = model.predict(image)
    # Plot detected objects on video frame
    res_plotted = res[0].plot()
    st_frame.image(res_plotted,caption='Detected Video',channels="BGR",use_column_width=True)

def infer_uploaded_video(model,src_video):
   
    if src_video:
        st.video(src_video)
    if src_video:
        if st.button("Execute"):
            with st.spinner("Running.."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False) as tfile:
                        tfile.write(src_video.read())
                        tfile.flush()  # Ensure all data is written

                    video_frames = []
                    # Open the video file and extract frames
                    video_clip = VideoFileClip(tfile.name)
                    for frame in video_clip.iter_frames(fps=video_clip.fps):
                        # Convert frame to PIL Image
                        pil_image = Image.fromarray(frame)
                        video_frames.append(pil_image)

                    st_frame = st.empty()
                    for frame in video_frames:
                        display_detected_frames(model, st_frame, frame)

                except Exception as e:
                    st.error(f"Error loading video: {e}")
                finally:
                    if os.path.exists(tfile.name):
                        os.remove(tfile.name)
   
def play_webcam(model):
    
    if st.sidebar.button('Detect Objects'):
        try:
            vid_cap = cv2.VideoCapture(0)
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    display_detected_frames(model,st_frame,image)
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading video: " + str(e))
                  
                        
                        
                        
                        
                        