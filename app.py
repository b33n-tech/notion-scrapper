import requests
from bs4 import BeautifulSoup
from docx import Document

# --- CONFIGURATION ---
notion_url = "TON_URL_NOTION_ICI"  # Remplace par l'URL publique de ta page Notion
output_file = "notion_page.docx"

# --- RÉCUPÉRATION DE LA PAGE ---
response = requests.get(notion_url)
if response.status_code != 200:
    raise Exception(f"Impossible de récupérer la page, statut {response.status_code}")

html_content = response.text

# --- EXTRACTION DU TEXTE ---
soup = BeautifulSoup(html_content, "html.parser")
# Récupère tout le texte visible
for script_or_style in soup(["script", "style"]):
    script_or_style.decompose()

text = soup.get_text(separator="\n")  # sépare par lignes

# Nettoyage simple : supprime les lignes vides
lines = [line.strip() for line in text.splitlines() if line.strip()]
clean_text = "\n".join(lines)

# --- ÉCRITURE DANS LE DOCX ---
doc = Document()
for line in lines:
    doc.add_paragraph(line)

doc.save(output_file)
print(f"Le contenu a été enregistré dans {output_file}")
