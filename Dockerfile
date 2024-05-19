# Base image with minimal dependencies
FROM python:3.12.3-slim
# Install system dependencies
# RUN apt-get update && \
#     apt-get install -y ffmpeg libsm6 libxext6 && \
#     apt-get clean && rm -rf /var/lib/apt/lists/*  

# Install Python packages in a specific order
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        libsm6 \
        libxext6 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir \
        numpy \
        pillow && \
    pip install --no-cache-dir \
        ipython\
        opencv-python \
        google-cloud-vision \
        streamlit && \
    pip install --no-cache-dir \
        torch torchvision --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir \
        ultralytics\
        moviepy

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . .

# Expose the required port
EXPOSE 8080

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py"]







# 2.94 GB
# # Base image with minimal dependencies
# FROM python:3.9-slim
# # Install Python dependencies
# RUN pip install pillow==10.3.0 
# RUN pip install ipython 
# RUN pip install numpy 
# RUN pip install opencv-python 
# RUN pip install google-cloud-vision 
# RUN pip install streamlit 
# RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
# RUN pip install ultralytics
# RUN pip install moviepy
# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
 
# # Working directory
# WORKDIR /app

# # Copy essential application files
# COPY . .

# # Expose Streamlit port (default 8501)
# EXPOSE 8501

# # Command to run your Streamlit app (replace 'app.py' with your actual file)
# CMD ["streamlit", "run", "app.py"]
