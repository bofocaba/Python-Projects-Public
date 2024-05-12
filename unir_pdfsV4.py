import streamlit as st
import fitz
import zipfile
import os
from PyPDF2 import PdfMerger
from io import BytesIO
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

output_zip = "c:/Users/bruba/Downloads/pdf_images.zip"
output_pdf = "c:/Users/bruba/Downloads/pdf_final.pdf"

def split_pdf_pages_to_images(documents):
    output_buffer = BytesIO()
    zip_buffer = BytesIO()
    zip_file = zipfile.ZipFile(zip_buffer, mode="w")

    for index, document in enumerate(documents):
        pdf_document = fitz.open(stream=document.read(), filetype="pdf")
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            image = page.get_pixmap()
            img = Image.frombytes("RGB", [image.width, image.height], image.samples)
            image_path = f"temp_page_{index + 1}_image_{page_num + 1}.png"
            img.save(image_path, format="PNG")
            with open(image_path, "rb") as img_file:
                image_bytes = img_file.read()
                zip_file.writestr(f"page_{index + 1}_image_{page_num + 1}.png", image_bytes)
            os.remove(image_path)  # Eliminar el archivo temporal

    zip_file.close()
    zip_buffer.seek(0)
    output_buffer.write(zip_buffer.read())
    output_buffer.seek(0)

    return output_buffer

def merge_pdfs(documents):
    merger = PdfMerger()

    for document in documents:
        merger.append(BytesIO(document.read()))

    output_buffer = BytesIO()
    merger.write(output_buffer)
    merger.close()

    output_buffer.seek(0)
    return output_buffer

def create_pdf_from_images(image_paths, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=letter)

    for image_path in image_paths:
        c.drawImage(image_path, 0, 0, width=letter[0], height=letter[1])
        c.showPage()

    c.save()

st.header("Procesador de PDF")
st.subheader("Selecciona la acción")

pdf_adjuntos = st.file_uploader(label="", accept_multiple_files=True)
accion = st.selectbox("Selecciona una acción", ["Separar PDF en imágenes", "Unir PDFs", "Crear PDF desde imágenes"])

if accion == "Separar PDF en imágenes":
    if st.button(label="Separar PDF en imágenes"):
        if len(pdf_adjuntos) <= 0:
            st.warning("Debes adjuntar al menos un PDF")
        else:
            images_data = split_pdf_pages_to_images(pdf_adjuntos)
            st.success("Las imágenes se han generado correctamente")
            st.download_button(label="Descargar imágenes", data=images_data, file_name="pdf_images.zip", mime="application/zip")

elif accion == "Unir PDFs":
    if st.button(label="Unir PDFs"):
        if len(pdf_adjuntos) <= 1:
            st.warning("Debes adjuntar al menos dos PDFs para unir")
        else:
            pdf_data = merge_pdfs(pdf_adjuntos)
            st.success("Los PDFs se han unido correctamente")
            st.download_button(label="Descargar PDF unido", data=pdf_data, file_name="pdf_final.pdf", mime="application/pdf")

elif accion == "Crear PDF desde imágenes":
    if st.button(label="Crear PDF desde imágenes"):
        if len(pdf_adjuntos) <= 0:
            st.warning("Debes adjuntar al menos una imagen en formato PNG")
        else:
            image_paths = []
            for image_file in pdf_adjuntos:
                if image_file.name.endswith(".png"):
                    with open(image_file.name, "wb") as f:
                        f.write(image_file.getvalue())
                    image_paths.append(image_file.name)
            if len(image_paths) > 0:
                output_pdf_path = "pdf_from_images.pdf"
                create_pdf_from_images(image_paths, output_pdf_path)
                with open(output_pdf_path, "rb") as pdf_file:
                    pdf_data = pdf_file.read()
                    st.success("El PDF se ha creado correctamente a partir de las imágenes")
                    st.download_button(label="Descargar PDF creado", data=pdf_data, file_name="pdf_from_images.pdf", mime="application/pdf")
                os.remove(output_pdf_path)
            else:
                st.warning("No se encontraron imágenes en formato PNG")

