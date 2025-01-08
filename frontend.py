import streamlit as st
import requests
from PIL import Image
import io
import base64

# Set up the Streamlit page
st.set_page_config(
    page_title="Moon Terrain Segmentation App",
    page_icon="🌕",
    layout="wide"
)

# Default Background Image Path
DEFAULT_BACKGROUND_IMAGE_PATH = "background_image/static_image_.jpg"

# Read the background image and convert it to base64
with open(DEFAULT_BACKGROUND_IMAGE_PATH, "rb") as bg_file:
    default_bg_image_base64 = base64.b64encode(bg_file.read()).decode()

# Add custom CSS for the background
st.markdown(
    f"""
    <style>
    .stApp {{
        background: url("data:image/webp;base64,{default_bg_image_base64}");
        background-size: cover;
        background-position: center;
    }}
    .stContainer {{
        background: rgba(0, 0, 0, 0.7);
        padding: 20px;
        border-radius: 10px;
    }}
    .black-transparent {{
        background: rgba(0, 0, 0, 0.7);
        padding: 15px;
        border-radius: 10px;
        color: white;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'home'

# Backend API endpoints
PREPROCESS_URL = "http://127.0.0.1:8000/preprocess/"
SEGMENT_URL = "http://127.0.0.1:8000/segment/"

# Session state for storing images
if 'preprocessed_image' not in st.session_state:
    st.session_state['preprocessed_image'] = None
if 'segmented_image' not in st.session_state:
    st.session_state['segmented_image'] = None
if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None

# Home Page Function
def show_home_page():
    st.markdown(
        """
        <div class="black-transparent">
            <h1>Welcome to Moon Terrain Segmentation App 🌘</h1>
            <p>
                Welcome to the Moon Terrain Segmentation App! This tool uses advanced image processing
                to analyze and segment images of the moon's surface.
            </p>
            <h3>Instructions:</h3>
            <ul>
                <li>Go to the Segmentation Page by clicking "Get Started".</li>
                <li>Upload an image of the moon's surface (accepted formats: JPG, PNG, BMP). Ensure the resolution is at least 480x480 pixels.</li>
                <li>The app will preprocess the image automatically.</li>
                <li>Click "Segment This Image" to perform the segmentation.</li>
                <li>The segmented image will be displayed alongside the preprocessed version.</li>
            </ul>
            <p>Click the button below to begin exploring the moon's terrain.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Button to navigate to Segmentation Page
    if st.button("Get Started"):
        st.session_state['current_page'] = 'segmentation'

# Segmentation Page Function
def show_segmentation_page():
    st.markdown('<div class="black-transparent"><h1>Moon Terrain Segmentation Page</h1></div>', unsafe_allow_html=True)
    
    # Upload an image
    st.markdown('<div class="black-transparent"><p>Upload an image of the moon\'s surface (min size: 480x480 pixels):</p></div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png", "bmp"])

    # Handle new uploads
    if uploaded_file is not None:
        if st.session_state['uploaded_file'] != uploaded_file:
            st.session_state['uploaded_file'] = uploaded_file
            st.session_state['preprocessed_image'] = None
            st.session_state['segmented_image'] = None

        # Automatically preprocess the image
        if st.session_state['preprocessed_image'] is None:
            with st.spinner("Processing..."):
                try:
                    files = {'file': uploaded_file.getvalue()}
                    response = requests.post(PREPROCESS_URL, files=files)
                    response.raise_for_status()
                    preprocessed_image = Image.open(io.BytesIO(response.content))
                    st.session_state['preprocessed_image'] = preprocessed_image
                except requests.exceptions.RequestException as e:
                    st.error(f"Error during preprocessing: {e}")

    # Show preprocessed image and segmentation button
    if st.session_state['preprocessed_image'] is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(st.session_state['preprocessed_image'], caption="Preprocessed Image", use_container_width=True)
            if st.button("Segment This Image"):
                with st.spinner("Segmenting..."):
                    try:
                        img_byte_arr = io.BytesIO()
                        st.session_state['preprocessed_image'].save(img_byte_arr, format='PNG')
                        img_byte_arr.seek(0)
                        files = {'file': img_byte_arr.getvalue()}
                        response = requests.post(SEGMENT_URL, files=files)
                        response.raise_for_status()
                        segmented_image = Image.open(io.BytesIO(response.content))
                        st.session_state['segmented_image'] = segmented_image
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error during segmentation: {e}")

        with col2:
            if st.session_state['segmented_image'] is not None:
                st.image(st.session_state['segmented_image'], caption="Segmented Image", use_container_width=True)

    # Button to return to the Home Page
    if st.button("Go Back"):
        st.session_state['current_page'] = 'home'

# Main Logic to Render Pages
if st.session_state['current_page'] == 'home':
    show_home_page()
elif st.session_state['current_page'] == 'segmentation':
    show_segmentation_page()
