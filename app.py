import streamlit as st
import easyocr
import numpy as np
import cv2
import pandas as pd
from io import BytesIO
from PIL import Image

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])  # add other languages if needed

st.title("📸 OCR Text Extractor")

# Upload images (single or multiple)
uploaded_files = st.file_uploader(
    "Upload image(s)", type=["png", "jpg", "jpeg"], accept_multiple_files=True
)

if uploaded_files:
    extracted_results = []

    for uploaded_file in uploaded_files:
        # Read image
        image = Image.open(uploaded_file).convert("RGB")
        img_array = np.array(image)

        # Run OCR
        results = reader.readtext(img_array)
        extracted_text = "\n".join([res[1] for res in results])

        # Show image + extracted text
        st.image(image, caption=uploaded_file.name, use_column_width=True)
        st.text_area(
            f"Extracted Text from {uploaded_file.name}",
            extracted_text,
            height=150,
        )

        extracted_results.append((uploaded_file.name, extracted_text))

    # --- DOWNLOAD OPTIONS ---
    if len(extracted_results) == 1:
        # Single file case
        filename, text = extracted_results[0]

        # TXT
        st.download_button(
            "Download as .txt",
            text,
            file_name="extracted.txt",
            mime="text/plain",
        )

        # (PDF disabled for ARM64)
        # If you later switch to fpdf2 or x64 Python, you can re-enable PDF export

    else:
        # Multiple files case → export as CSV
        df = pd.DataFrame(
            [{"filename": name, "text": text} for name, text in extracted_results]
        )
        csv_bytes = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download all results as .csv",
            csv_bytes,
            file_name="results.csv",
            mime="text/csv",
        )
