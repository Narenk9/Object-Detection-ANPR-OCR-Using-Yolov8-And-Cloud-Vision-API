# Object Detection, ANPR, and OCR Using YOLOv8 and Google Cloud Vision API

## Overview

This project is a web application that performs object detection, license plate detection, and Optical Character Recognition (OCR) on license plates using the Google Cloud Vision API. The frontend is built using the Streamlit open-source framework.

## Features

- **Object Detection:** Detects various objects within images using the YOLOv8 model.
- **License Plate Detection:** Specifically trained to detect license plates from images.
- **OCR on License Plates:** Uses Google Cloud Vision API to extract text from detected license plates.

## Datasets

- **Source:** The license plate dataset was sourced from [Roboflow](https://roboflow.com/).
- **Annotations:** The dataset includes annotated images.
  - **Train Set:** 1050 images
  - **Test Set:** 75 images
  - **Validation Set:** 75 images

## Model Training

- **Framework:** Utilized the Ultralytics YOLOv8 open-source package.
- **Specifications:**
  - **YOLOv8 Version:** 8.0.0
  - **Python Version:** 3.10.12
  - **PyTorch Version:** 2.2.1+cu121
  - **CUDA:** 0 (Tesla T4, 15102MiB)
  - **Platform:** Google Colab

## Deployment

- **Docker:** The application was containerized using a Dockerfile, resulting in a Docker image size of approximately 2.5GB.
- **Hosting:** Deployed using Google Cloud services, specifically Artifact Registry and Google Cloud Run.

## Installation and Usage

### Prerequisites

- Docker
- Google Cloud account with necessary permissions for Cloud Run and Artifact Registry
- Streamlit

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Narenk9/Object-Detection-ANPR-OCR-Using-Yolov8-And-Cloud-Vision-API.git
   cd Object-Detection-ANPR-OCR-Using-Yolov8-And-Cloud-Vision-API
   ```

2. **Build the Docker image:**

   ```bash
   docker build -t anpr-ocr-app .
   ```

3. **Run the Docker container:**

   ```bash
   docker run -p 8501:8501 anpr-ocr-app
   ```

4. **Access the application:**

   Open your web browser and navigate to `http://localhost:8501`.

## Deployment on Google Cloud Run

1. **Authenticate with Google Cloud:**

   ```bash
   gcloud auth login
   gcloud config set project [YOUR_PROJECT_ID]
   ```

2. **Push the Docker image to Artifact Registry:**

   ```bash
   gcloud builds submit --tag [REGION]-docker.pkg.dev/[YOUR_PROJECT_ID]/anpr-ocr-app/anpr-ocr-app
   ```

3. **Deploy to Cloud Run:**

   ```bash
   gcloud run deploy anpr-ocr-app --image [REGION]-docker.pkg.dev/[YOUR_PROJECT_ID]/anpr-ocr-app/anpr-ocr-app --platform managed --region [REGION] --allow-unauthenticated
   ```

4. **Access the deployed application:**

   The URL for the deployed application will be provided after successful deployment. Open it in your web browser.

## Contributing

Contributions are welcome! Please fork the repository and use a feature branch. Pull requests are gladly accepted.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Roboflow](https://roboflow.com/) for providing the license plate dataset.
- [Ultralytics](https://ultralytics.com/) for the YOLOv8 model.
- [Google Cloud](https://cloud.google.com/) for their Vision API and hosting services.
- [Streamlit](https://streamlit.io/) for the frontend framework.

---

This README provides a clear and detailed overview of your project, instructions for installation and deployment, and credits the resources and tools used.