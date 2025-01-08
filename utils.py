# Updated Utils Code
import io
from PIL import Image
from skimage.io import imread
import numpy as np

# Function to preprocess the image for the segmentation model
def preprocess_image(image_file):
    # Target height and width for cropping
    H, W = 480, 480

    # Read the image file
    img = imread(image_file)

    # Check if the image dimension criteria is matched
    original_height, original_width, channels = img.shape
    if original_height < H or original_width < W:
        raise ValueError(f"Image must be at least 480x480 pixels. Provided Image Dimensions are small: {img.shape}")
    elif channels != 3:
        raise ValueError(f"The channels in the input image must be 3. You have provided: {channels} channels!")

    # Crop the image to first 480 by 480 pixels
    img_resized = img[:H, :W, :]

    # Normalize the image in range of 0-1 and convert it to float32
    normalized_img = img_resized / 255.0
    float32_img = normalized_img.astype(np.float32)

    return float32_img

# Function to map the colors for segmentation classes
def get_color_map():
    return np.array([
        [0, 0, 0],       # Class 0: Black (Lunar Soil / Background)
        [255, 0, 0],     # Class 1: Red (Large Rocks)
        [0, 255, 0],     # Class 2: Green (Sky)
        [0, 0, 255]      # Class 3: Blue (Small Rocks)
    ], dtype=np.uint8)
