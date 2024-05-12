import streamlit as st
from PIL import Image
from rembg import remove
import io
import os

def process_image(image_uploaded):
    image = Image.open(image_uploaded)
    proccesed_imagen = remove_backgorund(image)
    
    return proccesed_imagen

def remove_backgorund(image):
    image_byte = io.BytesIO()
    image.save(image_byte, format="PNG")
    image_byte.seek(0)
    proccesed_image_bytes = remove(image_byte.read())
    
    return Image.open(io.BytesIO(proccesed_image_bytes))

st.header("Background removal APP")
st.subheader("Upload an image")
upload_image = st.file_uploader("Choose an image...", type = ["jpg", "jpeg", "png"])

if upload_image is not None:
    st.image(upload_image, caption="Imagen subida", use_column_width=True)
    remove_button=st.button(label="Quitar fondo")
    
    if remove_button:
        proccesed_image = process_image(upload_image)
        st.image(proccesed_image, caption="Backgroud Removed", use_column_width=True)
        proccesed_image.save("processed_image.png")
        
        with open("processed_image.png", "rb") as f:
            image_data = f.read()
        
        st.download_button("Download proccesed image", data=image_data, file_name="processed_image.png")
        os.remove("processed_image.png")