import streamlit as st
import easyocr
import numpy as np
import pandas as pd
from PIL import Image
from io import BytesIO
import zipfile

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])  # Add more languages if needed

st.title("📸 OCR Text Extractor")

# --- Upload Images with drag-and-drop ---
uploaded_files = st.file_uploader(
    "Upload image(s) (drag & drop supported)", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

if uploaded_files:
    extracted_results = []

    # --- User-friendly OCR message ---
    status_text = st.empty()
    status_text.text("Processing OCR...")

    # --- Progress bar ---
    my_bar = st.progress(0)
    
    for i, uploaded_file in enumerate(uploaded_files):
        # Read image
        image = Image.open(uploaded_file).convert("RGB")
        img_array = np.array(image)

        # Run OCR
        results = reader.readtext(img_array)
        extracted_text = "\n".join([res[1] for res in results])

        # Show image + extracted text
        st.image(image, caption=uploaded_file.name, use_column_width=True)
        st.text_area(f"Extracted Text from {uploaded_file.name}", extracted_text, height=150)

        extracted_results.append((uploaded_file.name, extracted_text))

        # Update progress
        my_bar.progress((i+1)/len(uploaded_files))

    # Remove progress bar and status message
    my_bar.empty()
    status_text.empty()

    # --- DOWNLOAD OPTIONS ---
    if len(extracted_results) == 1:
        filename, text = extracted_results[0]
        st.download_button("Download as .txt", text, file_name=f"{filename}.txt", mime="text/plain")
    
    else:
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for filename, text in extracted_results:
                zip_file.writestr(f"{filename}.txt", text)
        zip_buffer.seek(0)

        st.download_button(
            "Download all results as ZIP",
            zip_buffer,
            file_name="extracted_texts.zip",
            mime="application/zip"
        )
