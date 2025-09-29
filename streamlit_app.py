import streamlit as st
from PIL import Image
import pytesseract
import os

st.title("My OCR App")
st.write("Upload an image and get the extracted text using Tesseract OCR.")

# --- Set Tesseract path for Windows ---
# Change this path if your Tesseract is installed elsewhere
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Open the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Extract text
    st.subheader("Extracted Text")
    text = pytesseract.image_to_string(image)
    
    if text.strip() == "":
        st.write("No text found in the image.")
    else:
        st.text(text)
