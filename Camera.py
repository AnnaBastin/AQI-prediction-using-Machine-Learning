import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import io

def run():

    # 1. Load AI Model
    @st.cache_resource
    def load_ai_model():
        current_folder = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_folder, 'camera_aqi_model.keras')

        if not os.path.exists(model_path):
            st.error(f"❌ Model file not found at: {model_path}")
            return None

        try:
            return tf.keras.models.load_model(model_path, compile=False)
        except Exception as e:
            st.error(f"🛑 Error loading model: {e}")
            return None

    model = load_ai_model()

    CLASS_NAMES = [
        "Good (0-50) 🟢",
        "Moderate (51-100) 🟡",
        "Unhealthy for Sensitive Groups (101-150) 🟠",
        "Unhealthy (151-200) 🔴",
        "Very Unhealthy (201-300) 🟣",
        "Severe (301+) 🟤"
    ]

    st.title("📷 AI Camera AQI Detector")
    st.write("Point your camera at the sky to estimate air quality visually.")

    if model is None:
        return

    st.markdown("---")

    # Input method
    input_method = st.radio(
        "Choose image input method",
        ["📷 Camera", "🖼️ Choose Image File"]
    )

    image_file = None

    # Camera Input
    if input_method == "📷 Camera":
        camera_photo = st.camera_input("Take a picture of the environment")

        if camera_photo is not None:
            image_file = camera_photo

    # Upload Input
    elif input_method == "🖼️ Choose Image File":

        uploaded_file = st.file_uploader(
            "Upload an image or document",
            type=["jpg", "jpeg", "png", "webp", "bmp", "pdf"]
        )

        if uploaded_file is not None:

            if uploaded_file.type == "application/pdf":

                st.warning("PDF detected. Only the first page will be used.")

                import fitz

                pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                page = pdf.load_page(0)
                pix = page.get_pixmap()

                img_bytes = pix.tobytes("png")
                image_file = io.BytesIO(img_bytes)

            else:
                image_file = uploaded_file

    # Prediction
    if image_file is not None:

        st.write("🧠 AI is analyzing...")

        image = Image.open(image_file).convert('RGB')
        image = image.resize((224, 224))

        img_array = np.array(image) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)

        predicted_index = np.argmax(predictions[0])
        confidence = np.max(predictions[0]) * 100

        predicted_label = CLASS_NAMES[predicted_index]

        st.subheader("📊 Results")

        st.success(f"Predicted Air Quality: {predicted_label}")
        st.info(f"AI Confidence: {confidence:.2f}%")
