import streamlit as st
import numpy as np
import tensorflow as tf
from streamlit_drawable_canvas import st_canvas
from PIL import Image

# page config
st.set_page_config(
    page_title="MNIST Digit Recognizer",
    page_icon="??",
    layout="centered"
)

st.title("MNIST Digit Recognizer")
st.write("Draw a digit (0-9) and let the AI model predict it.")

# load model
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("model.keras", compile=False)

model = load_model()

# canvas
canvas_result = st_canvas(
    stroke_width=15,
    stroke_color="white",
    background_color="black",
    height=280,
    width=280,
    drawing_mode="freedraw",
    key="canvas",
)

col1, col2 = st.columns(2)

if canvas_result.image_data is not None:

    img = canvas_result.image_data

    img = np.mean(img, axis=2)

    img = Image.fromarray(img.astype("uint8"))
    img = img.resize((28,28))

    img_array = np.array(img)

    processed = img_array / 255.0
    processed = processed.reshape(1,28,28,1)

    prediction = model.predict(processed)

    digit = np.argmax(prediction)
    confidence = np.max(prediction)

    with col1:
        st.subheader("Prediction")
        st.success(f"Digit: {digit}")
        st.write(f"Confidence: {confidence:.2f}")

    with col2:
        st.subheader("Processed Image")
        st.image(img_array, width=150)

    st.subheader("Prediction Probabilities")
    st.bar_chart(prediction[0])