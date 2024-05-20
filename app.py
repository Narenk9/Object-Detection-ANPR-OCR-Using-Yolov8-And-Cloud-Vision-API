# Use cProfile to check slow code
# External packages
import streamlit as st
from google.cloud import vision
from pathlib import Path
import numpy as np
import PIL
from IPython.display import display
from PIL import Image
from io import BytesIO

# Local modules
import components
import helper
# Setting page layout
st.set_page_config(
    page_title ="ANPR using Yolo",
    page_icon="🚀",
    layout ="wide",
    initial_sidebar_state='expanded'
)
client = vision.ImageAnnotatorClient.from_service_account_json('anpryolo.json')
st.sidebar.header("Things you can do!!")
model_type = st.sidebar.radio('Select', ['Object Detection','License Plate Detection','ANPR + OCR'])

@st.cache_resource
def get_model_path(model_type):
    if model_type=='Object Detection':
        return Path(components.object_model)
    else:
        return Path(components.anpr_model)
    
# Load Pre-Trained Model
@st.cache_resource
def load_model(model_path):
    try:
        model = helper.load_model(model_path)
        return model
    except Exception as e:
        st.error(f"Unable to load model. Check the specified Path:{model_path}")
        st.error(e)

st.sidebar.header("Types of Sources")

if model_type=='License Plate Detection':
    st.header("Automatic Number Plate Recognition using Yolo",divider='rainbow')
    src_radio = st.sidebar.radio("Select",['Image','Video'])
    model_path = get_model_path(model_type)
    model = load_model(model_path)
    src_image =None
    # If Image is selected
    if src_radio=='Image':
        src_image = st.sidebar.file_uploader("Choose an image...",type=("jpg", "jpeg", "png", 'bmp', 'webp'))
        
        col1,col2 = st.columns(2)
        with col1: # Showing default and User's uploaded image on web
            try:
                if src_image is None:
                    default_image_path = str(components.default_image)
                    with open(default_image_path, 'rb') as f:
                        image_data = f.read()
                    st.image(image_data,caption='Default Image')
                else:
                    uploaded_image = PIL.Image.open(src_image)
                    st.image(src_image,caption="Image That you uploaded!")
            except Exception as e:
                st.error("Error occurred while opening the image.")
                st.error(e)
        with col2: # Prediction of input image
            if src_image is None:
                default_detected_image_path = str(components.default_detect_image)
                default_detected_image = PIL.Image.open(default_detected_image_path)
                st.image(default_detected_image_path, caption='Default Detected Image')
            else:
                if st.sidebar.button('Detect Objects'):
                    # predict user's image
                    res = model.predict(uploaded_image)
                    boxes = res[0].boxes
                    if len(boxes) == 0:
                        st.error("No objects detected in the image.")
                    else:
                        res_plotted = res[0].plot()[:, :, ::-1]
                        st.image(res_plotted, caption='Detected Image',
                                use_column_width=True)
                        try:
                            with st.expander("Detection Results"):
                                for box in boxes:
                                    st.write(box.data)
                        except Exception as ex:
                            st.write("No image is uploaded yet!")
    else:  
        src_video = st.sidebar.file_uploader(label="Choose a video...") 
        
        try:
            if src_video is None:
                pass
                #st.video(r'media/anpr_detect.mp4',autoplay=True,loop=True)
                
        except Exception as e:
            st.error("Error occurred while opening Video.")
            st.error(e)
        if src_video:
            helper.infer_uploaded_video(model,src_video)
elif model_type=='OCR':
    
    st.header("ANPR + OCR using GCP Cloud Vision",divider='rainbow')
    
    src_image = st.sidebar.file_uploader("Choose an image...",type=("jpg", "jpeg", "png", 'bmp', 'webp'))
    model_path = get_model_path(model_type)
    model = load_model(model_path) 
    col1,col2 = st.columns(2)
    with col1: # Showing default and User's uploaded image on web
            try:
                if src_image is None:
                    default_detected_image_path = str(components.default_detect_image)
                    default_detected_image = PIL.Image.open(default_detected_image_path)
                    st.image(default_detected_image_path, caption='Default Detected Image')
                else:
                    uploaded_image = PIL.Image.open(src_image)
                    st.image(src_image,caption="Image That you uploaded!")
            except Exception as e:
                st.error("Error occurred while opening the image.")
                st.error(e)
    with col2: # Prediction of input image
        if src_image is None:
            pass
        else:
            if st.sidebar.button('Detect Objects'):
                            # predict user's image
                res = model(uploaded_image)
                
                boxes = res[0].boxes
                if len(boxes) == 0:
                    st.error("No objects detected in the image.")
                else:
                    res_plotted = res[0].plot()[:, :, ::-1]
                    st.image(res_plotted, caption='Detected Image',
                            use_column_width=True)
                    try:
                        with st.expander("Detection Results"):
                            for box in boxes:
                                st.write(box.data)
                    except Exception as ex:
                        st.write("No image is uploaded yet!")
                        # Extracting values from the tensor
    
                    x_min, y_min, x_max, y_max, confidence_score, class_index = map(int,box.data[0].tolist())
                                
                    # Convert the uploaded image to a NumPy array
                    uploaded_image_array = np.array(uploaded_image)

                    # Crop the region of interest (ROI) from the uploaded image array
                    roi_image_array = uploaded_image_array[y_min:y_max, x_min:x_max]

                    # Convert the cropped ROI image array back to PIL Image
                    roi_image = Image.fromarray(roi_image_array)

                    # Display the ROI image
                    st.image(roi_image, caption='Region of Interest (ROI) Image')
                    # Convert ROI to bytes efficiently using NumPy
                    with BytesIO() as output:
                        roi_image_pil = Image.fromarray(roi_image_array)
                        roi_image_pil.save(output, format='JPEG')
                        img_bytes = output.getvalue()                   
                    # Perform OCR using Google Cloud Vision API
                    try:
                        image = vision.Image(content=img_bytes)
                        response = client.text_detection(image=image)
                        texts = response.text_annotations
                        # Extract OCR result
                        if texts:
                            license_plate_text = texts[0].description
                            st.success("Text Detected using Google Cloud Vision API")
                            st.success(license_plate_text)
                            st.balloons()
                        else:
                            st.error("No text found in the region")
                    except Exception as e:
                       st.error("Google Cloud Vision API is disabled by Owner")
else:
    st.header('Object Detection using Yolo', divider='rainbow')
    src_radio = st.sidebar.radio("Select",['Image','Video','Webcam'])
    model_path = get_model_path(model_type)
    model = load_model(model_path)
    src_image =None
    # If Image is selected
    if src_radio=='Image':
        src_image = st.sidebar.file_uploader("Choose an image...",type=("jpg", "jpeg", "png", 'bmp', 'webp'))
        
        col1,col2 = st.columns(2)
        with col1: # Showing default and User's uploaded image on web
            try:
                if src_image is None:
                    image_path = str(components.default_obj1)
                    with open(image_path, 'rb') as f:
                        image_data = f.read()
                    st.image(image_data,caption='Default Image')
                else:
                    uploaded_image = PIL.Image.open(src_image)
                    st.image(src_image,caption="Image That you uploaded!")
            except Exception as e:
                st.error("Error occurred while opening the image.")
                st.error(e)
        with col2: # Prediction of input image
            if src_image is None:
                default_detected_image_path = str(components.default_obj2)
                default_detected_image = PIL.Image.open(default_detected_image_path)
                st.image(default_detected_image_path, caption='Default Detected Image')
            else:
                if st.sidebar.button('Detect Objects'):
                    # predict user's image
                    res = model.predict(uploaded_image)
                    boxes = res[0].boxes
                    if len(boxes) == 0:
                        st.error("No objects detected in the image.")
                    else:
                        res_plotted = res[0].plot()[:, :, ::-1]
                        st.image(res_plotted, caption='Detected Image',
                                use_column_width=True)
                        try:
                            with st.expander("Detection Results"):
                                for box in boxes:
                                    st.write(box.data)
                        except Exception as ex:
                            st.write("No image is uploaded yet!")
    elif src_radio=='Video':  
        src_video = st.sidebar.file_uploader(label="Choose a video...") 
        try:
            if src_video is None:
                # video_path = str(components.detect_obj_video)
                st.video(r'.\media\default _detect_object.mp4',autoplay=True,loop=True)    
                
        except Exception as e:
            st.error("Error occurred while opening Video.")
            st.error(e)
        if src_video:
            helper.infer_uploaded_video(model,src_video)
    else:
        helper.play_webcam(model)
profile_pic_path = str(components.profile_pic)
with open(profile_pic_path, 'rb') as f:
    image_data = f.read()
st.sidebar.image(image_data,caption='Made By Naren Karthikeya',use_column_width="auto")# Model options
