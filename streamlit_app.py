import streamlit as st
from PIL import Image
import easyocr

st.title("My OCR App")
st.write("Upload an image and get the extracted text using EasyOCR.")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Open image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Initialize EasyOCR reader (English)
    reader = easyocr.Reader(['en'])
    
    # Extract text
    st.subheader("Extracted Text")
    results = reader.readtext(image)
    
    if len(results) == 0:
        st.write("No text found in the image.")
    else:
        extracted_text = "\n".join([res[1] for res in results])
        st.text(extracted_text)
