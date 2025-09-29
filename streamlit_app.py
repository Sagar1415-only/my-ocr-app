import streamlit as st
from PIL import Image
import easyocr

st.title("My OCR App")
st.write("Upload an image and get the extracted text using EasyOCR.")

# Cache the EasyOCR reader to avoid reloading models on every run
@st.cache_resource
def get_reader():
    return easyocr.Reader(['en'])

reader = get_reader()

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)
    
    st.subheader("Extracted Text")
    results = reader.readtext(image)
    
    if len(results) == 0:
        st.write("No text found in the image.")
    else:
        extracted_text = "\n".join([res[1] for res in results])
        st.text(extracted_text)
