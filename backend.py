from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
from PIL import Image
import numpy as np
import io

from utils import preprocess_image, get_color_map

# Initialize FastAPI
app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Load the pre-trained model for segmentation
model_path = 'LunarModel.h5'  
try:
    model = tf.keras.models.load_model(model_path, compile=False)
except Exception as e:
    raise RuntimeError(f"Failed to load the model. Error: {str(e)}")

# Root Endpoint
@app.get("/")
async def read_root():
    return {"status": "Backend is running!"}

# Preprocess Image Endpoint
@app.post("/preprocess/")
async def preprocess_image_endpoint(file: UploadFile = File(...)):
    try:
        # Read the image file into a BytesIO object
        image_bytes = await file.read()
        image_file = io.BytesIO(image_bytes)

        # Preprocess the image
        image_array = preprocess_image(image_file)

        # Convert the preprocessed image to a PIL Image
        preprocessed_pil_image = Image.fromarray((image_array * 255).astype(np.uint8))

        # Save the preprocessed image to a BytesIO object
        preprocessed_img_byte_arr = io.BytesIO()
        preprocessed_pil_image.save(preprocessed_img_byte_arr, format="PNG")
        preprocessed_img_byte_arr.seek(0)

        return StreamingResponse(preprocessed_img_byte_arr, media_type="image/png")

    except Exception as e:
        return JSONResponse(content={"error": f"Preprocessing failed: {str(e)}"}, status_code=500)

# Segment Image Endpoint
@app.post("/segment/")
async def segment_lunar_terrain(file: UploadFile = File(...)):
    try:
        # Read the preprocessed image file into a BytesIO object
        image_bytes = await file.read()
        image_file = io.BytesIO(image_bytes)

        # Load the image as a numpy array
        preprocessed_image = Image.open(image_file)
        image_array = np.array(preprocessed_image) / 255.0  # Normalize to [0, 1]

        # Perform segmentation using the loaded lunar model
        pred_mask = model.predict(np.expand_dims(image_array, axis=0), verbose=0)
        pred_mask = np.argmax(pred_mask, axis=-1)
        pred_mask = pred_mask[0]  # Remove batch dimension

        # Get color map and apply to pred_mask
        color_map = get_color_map()
        if pred_mask.max() >= len(color_map):
            raise ValueError("Predicted mask contains invalid class indices.")
        pred_mask_colored = color_map[pred_mask]

        # Convert the predicted mask to a PIL Image
        segmented_pil_image = Image.fromarray(pred_mask_colored)

        # Save the segmented image to a BytesIO object
        segmented_img_byte_arr = io.BytesIO()
        segmented_pil_image.save(segmented_img_byte_arr, format="PNG")
        segmented_img_byte_arr.seek(0)

        return StreamingResponse(segmented_img_byte_arr, media_type="image/png")

    except Exception as e:
        return JSONResponse(content={"error": f"Segmentation failed: {str(e)}"}, status_code=500)
