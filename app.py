import streamlit as st
from PIL import Image
import numpy as np
import easyocr

st.set_page_config(page_title="✍️ Handwriting OCR", layout="centered")

st.title("✍️ Handwriting OCR App")
st.write("Upload or capture an image of handwriting and extract text using EasyOCR.")

@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

reader = load_reader()

uploaded = st.file_uploader("Upload an image", type=["png","jpg","jpeg"])
camera = st.camera_input("Or take a photo")

source = camera or uploaded

if source:
    img = Image.open(source).convert("RGB")
    st.image(img, caption="Input Image", use_column_width=True)

    st.info("Processing handwriting...")
    results = reader.readtext(np.array(img))

    if results:
        st.subheader("Recognized text:")
        text_out = " ".join([t[1] for t in results])
        st.code(text_out)
    else:
        st.warning("No text detected.")
else:
    st.info("Please upload or capture an image to start.")
