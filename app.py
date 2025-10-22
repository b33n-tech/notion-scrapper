import streamlit as st
import requests
from bs4 import BeautifulSoup
from docx import Document
from io import BytesIO

st.title("Notion Page → Word")

notion_url = st.text_input("URL de la page Notion publique:")

if st.button("Générer DOCX") and notion_url:
    try:
        response = requests.get(notion_url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
        
        text = soup.get_text(separator="\n")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        
        doc = Document()
        for line in lines:
            doc.add_paragraph(line)
        
        # Préparer le DOCX en mémoire
        doc_io = BytesIO()
        doc.save(doc_io)
        doc_io.seek(0)
        
        st.download_button(
            label="Télécharger le fichier Word",
            data=doc_io,
            file_name="notion_page.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        st.success("DOCX généré avec succès !")
    except Exception as e:
        st.error(f"Erreur : {e}")
