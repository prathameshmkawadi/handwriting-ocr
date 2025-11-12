import streamlit as st
from PIL import Image
import numpy as np
import easyocr, os

# force model download during build
if not os.path.exists(os.path.expanduser("~/.EasyOCR")):
    reader_tmp = easyocr.Reader(['en'], gpu=False)
    del reader_tmp


st.set_page_config(page_title="✍️ Handwriting OCR", layout="centered")

st.title("✍️ Handwriting OCR App")
st.write("Upload or capture an image of handwriting to extract text using EasyOCR.")

@st.cache_resource
def load_reader():
    # EasyOCR downloads model files once and caches them
    return easyocr.Reader(['en'], gpu=False)

reader = load_reader()

uploaded = st.file_uploader("Upload an image", type=["png","jpg","jpeg"])
camera = st.camera_input("Or take a photo")

source = camera or uploaded

if source:
    try:
        img = Image.open(source).convert("RGB")
        st.image(img, caption="Input Image", use_column_width=True)

        st.info("Processing handwriting... please wait ⏳")
        results = reader.readtext(np.array(img))

        if results:
            st.subheader("Recognized Text:")
            full_text = " ".join([t[1] for t in results])
            st.code(full_text)
        else:
            st.warning("No text detected. Try a clearer image.")
    except Exception as e:
        st.error(f"⚠️ OCR failed: {e}")
else:
    st.info("Please upload or capture an image to start.")
