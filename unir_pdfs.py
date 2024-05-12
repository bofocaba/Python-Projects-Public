import streamlit as st
import PyPDF2
from io import BytesIO

output_pdf = "c:/Users/bruba/Downloads/pdf_final.pdf"

def unir_pdfs(output_path, documents):
    pdf_final = PyPDF2.PdfMerger()

    for document in documents:
        pdf_final.append(document)

    # Crea un archivo de bytes en memoria
    output_buffer = BytesIO()
    pdf_final.write(output_buffer)
    # Reinicia el cursor del archivo a la posición 0 para permitir su lectura
    output_buffer.seek(0)
    return output_buffer

st.header("Unir PDF")
st.subheader("Adjuntar PDFs para unir")

pdf_adjuntos = st.file_uploader(label="", accept_multiple_files=True)

unir = st.button(label="Unir PDFs")

if unir:
    if len(pdf_adjuntos) <= 1:
        st.warning("Debes adjuntar más de un PDF")
    else:
        pdf_data = unir_pdfs(output_pdf, pdf_adjuntos)
        st.success("Desde aquí puedes descargar el PDF final")
        st.download_button(label="Descargar PDF final", data=pdf_data, file_name="pdf_final.pdf", mime="application/pdf")


