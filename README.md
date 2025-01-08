# Moon Terrain Segmentation 🌕

This project focuses on segmenting lunar terrain images to identify hazardous rocks that might pose a threat to lunar rovers. By leveraging deep learning and computer vision, it provides a robust pipeline for preprocessing, training, and deploying a segmentation model.

## 🚀 Key Features
- **UNet with ResNet-34 Backbone**: State-of-the-art architecture for image segmentation with a transfer learning backbone.
- **High Accuracy**: Achieves superior performance in predicting hazardous rock locations on lunar surfaces using the Intersection over Union (IoU) metric.
- **Preprocessing Pipeline**: Automated resizing, normalization, and one-hot encoding for lunar images.
- **Scalable Deployment**: Built-in support for API deployment using FastAPI and visualization through Streamlit.

## ⚙️ Setup and Installation

Follow these steps to set up the project locally:

### Clone the Repository
```bash
git clone <repository_url>
cd <repository_directory>
```

### Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the API
Start the FastAPI backend for predictions:
```bash
uvicorn main:app --reload
```
Access the API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### Visualize Results
Optionally, use Streamlit to upload images and view the segmented masks:
```bash
streamlit run app.py
```

##  Training Details

### Dataset
The model was trained on lunar terrain datasets containing labeled images for segmentation. Images were preprocessed to dimensions of 480x480 pixels, normalized, and augmented.

### Model Architecture
- **UNet**: A convolutional neural network tailored for semantic segmentation tasks.
- **Backbone**: ResNet-34 for enhanced feature extraction.
- **Optimizer**: Adam optimizer with learning rate scheduling.
- **Loss Function**: Categorical crossentropy combined with IoU metric for precise segmentation.

### Training Pipeline
1. **Preprocessing:**
   - Cropping and resizing images to a consistent size.
   - One-hot encoding for multi-class segmentation masks.
2. **Callbacks:**
   - `EarlyStopping` to prevent overfitting.
   - `ModelCheckpoint` to save the best-performing model.
3. **Metrics:**
   - IoU Score for evaluating segmentation quality.

## 🌐 API Endpoints

### Root Endpoint
**GET /**
- Returns a JSON response to verify the server status.

### Preprocess Image
**POST /preprocess/**
- Accepts a lunar image and returns the preprocessed image.

### Segment Terrain
**POST /segment/**
- Accepts a preprocessed image and returns the segmented mask.

## 📚 Acknowledgments
- **TensorFlow/Keras**: For building and training the deep learning model.
- **segmentation_models**: For providing efficient UNet implementations.
- **FastAPI**: For creating an interactive backend API.
- **Streamlit**: For building an intuitive front-end for user interaction.

