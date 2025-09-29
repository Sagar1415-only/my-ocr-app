import streamlit as st
from PIL import Image
import easyocr

st.title("My OCR App")
st.write("Upload an image and get the extracted text using EasyOCR.")

# Cache the EasyOCR reader to avoid reloading models
@st.cache_resource
def get_reader():
    return easyocr.Reader(['en'])

reader = get_reader()

# Preprocessing function
def preprocess_image(image):
    image = image.convert("L")
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    image = image.filter(ImageFilter.MedianFilter(size=3))
    return image

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Preprocess image
    processed_image = preprocess_image(image)
    
    st.image(processed_image, caption='Processed Image', use_container_width=True)
    
    st.subheader("Extracted Text")
    results = reader.readtext(processed_image)
    
    if len(results) == 0:
        st.write("No text found in the image.")
    else:
        extracted_text = "\n".join([res[1] for res in results])
        st.text(extracted_text)
