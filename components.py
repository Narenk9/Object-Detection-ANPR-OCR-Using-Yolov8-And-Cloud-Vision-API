from pathlib import Path
import sys

# Get the absolute path of the current file (only works in .py files) - path to this file ./settings.py
file_path = Path(__file__).resolve()

# Get the parent directory of the current file (main file: /yolov8-streamlit)
root_path = file_path.parent

# Add the root path to the sys.path list if it is not already there : allows for things like helper.process_license_plate()
if root_path not in sys.path:
    sys.path.append(str(root_path))

# Get the relative path of the root directory with respect to the main folder (basically IMAGES_DIR = ../yolov8-streamlit/'images')
root = root_path.relative_to(Path.cwd())

# Media Config
media_dir = root/'media'

default_image = media_dir/'default_image.jpg'
default_detect_image = media_dir/'default_detect_image.jpg'
# ANPR Detection default video
anpr_vid = media_dir/'anpr_detect.mp4'
# Object Detection Default Video
detect_obj_video = media_dir/'default_video_object.mp4'

# Object Detection Default Images
default_obj1 = media_dir/'obj1.jpg'
default_obj2 = media_dir/'obj2.jpg'
# About me
profile_pic = media_dir/'portrait.jpg'
# ML Configuration
model_dir = root/'weights'
object_model = model_dir / 'yolov8n.pt'
anpr_model = model_dir / 'best.pt'
