# Base image with minimal dependencies
FROM python:3.12.3-slim
# Expose the required port
EXPOSE 8080
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
# Command to run the Streamlit app
ENTRYPOINT ["streamlit", "run", "app.py", "–server.port=8080", "--server.fileWatcherType", "none"]





