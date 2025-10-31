from fastapi import uploadedfile
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import io 

def extract_text(file:uploadedfile):
    content=file.file.read()
    name=file.filename.lower()

    if name.endswith('.pdf'):
        reader=PdfReader(io.BytesIO(content))
        texts=[]

        for page in reader.pages:
            try:
                page_text=page.extract_text()

                if page_text:
                    texts.append(page_text.strip())
            except:
                continue 
        return "\n".join(texts)



