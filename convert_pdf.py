import os
from PyPDF2 import PdfReader

pdf_folder = "knowledge_base"
txt_folder = "knowledge_base_txt"

os.makedirs(txt_folder, exist_ok=True)

for file in os.listdir(pdf_folder):
    if file.endswith(".pdf"):
        path = os.path.join(pdf_folder, file)
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        txt_path = os.path.join(txt_folder, file.replace(".pdf", ".txt"))
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)

print("✅ PDFs converted to text in", txt_folder)
