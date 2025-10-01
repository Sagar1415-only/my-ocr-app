# =========================
# Imports
# =========================
import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
import cv2
import easyocr

# =========================
# App Title
# =========================
st.title("🖼️ Efficient OCR App (CPU-Friendly)")
st.write("Upload an image and get extracted text using EasyOCR (English, Hindi, Kannada).")

# =========================
# Language Selection
# =========================
language = st.selectbox("Select OCR Language", ["English", "Hindi", "Kannada"])
lang_code = {"English": "en", "Hindi": "hi", "Kannada": "kn"}[language]

# =========================
# Cache EasyOCR Reader
# =========================
@st.cache_resource
def get_reader(lang_code):
    return easyocr.Reader([lang_code])

reader = get_reader(lang_code)

# =========================
# Resize image to avoid memory issues
# =========================
def resize_image(image, max_dim=1024):
    w, h = image.size
    scale = min(max_dim / w, max_dim / h, 1)  # scale <= 1
    new_w, new_h = int(w * scale), int(h * scale)
    return image.resize((new_w, new_h))

# =========================
# English/Hindi preprocessing
# =========================
def preprocess_image(image):
    image = image.convert("L")
    image_np = np.array(image)

    # Slight denoise
    image_np = cv2.medianBlur(image_np, 3)

    # Adaptive threshold
    image_np = cv2.adaptiveThreshold(
        image_np, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )

    # Convert to PIL
    processed_image = Image.fromarray(image_np)

    # Enhance contrast & sharpness
    processed_image = ImageEnhance.Contrast(processed_image).enhance(1.8)
    processed_image = ImageEnhance.Sharpness(processed_image).enhance(1.5)

    return processed_image

# =========================
# Kannada-specific preprocessing
# =========================
def preprocess_kannada_image(image):
    image_np = np.array(image.convert("L"))

    # CLAHE contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    image_np = clahe.apply(image_np)

    # Mild denoise
    image_np = cv2.medianBlur(image_np, 3)

    # Convert back to PIL
    processed_image = Image.fromarray(image_np)

    return processed_image

# =========================
# Upload image
# =========================
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Open image
    original_image = Image.open(uploaded_file)

    # Resize to max dimension 1024px for CPU efficiency
    resized_image = resize_image(original_image, max_dim=1024)

    # Preprocess based on language
    if lang_code == "kn":
        processed_image = preprocess_kannada_image(resized_image)
    else:
        processed_image = preprocess_image(resized_image)

    processed_image_np = np.array(processed_image)

    # Display images side by side
    col1, col2 = st.columns(2)
    col1.image(resized_image, caption="Original Image", width=300)
    col2.image(processed_image, caption="Processed Image", width=300)

    # =========================
    # OCR Extraction
    # =========================
    results = reader.readtext(processed_image_np)

    # Filter short/empty results
    extracted_text_list = [res[1] for res in results if len(res[1].strip()) > 1]

    st.subheader("Extracted Text")
    if not extracted_text_list:
        st.write("No text found in the image.")
    else:
        extracted_text = "\n".join(extracted_text_list)
        st.text_area("Extracted Text", extracted_text, height=400)

        # =========================
        # Download button
        # =========================
        st.download_button(
            label="Download Extracted Text",
            data=extracted_text,
            file_name="extracted_text.txt",
            mime="text/plain"
        )
