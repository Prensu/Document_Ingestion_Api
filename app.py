from fastapi import uploadedfile
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import re
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

#now chunking strategies 
def chunk_fixed(text,max_chars=1000,overlap=200):
    chunks=[]
    start=0

    while start < len(text):
        end=start + max_chars
        chunk=text[start:end]
        chunks.append(chunk)

        start += max_chars - overlap
    return chunks

def chunk_sentence(text,max_chars500,overlap=100):
    from nltk.tokenize import sent_tokenize
    sentences=sent_tokenize(text)
    chunks=[]
    current_chunk=""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_chars:
            current_chunk += " " + sentence if current_chunk else sentence
        else:
            chunks.append(current_chunk)
            current_chunk=sentence

    if current_chunk:
        chunks.append(current_chunk)

    # Handle overlap
    if overlap > 0 and len(chunks) > 1:
        overlapped_chunks=[]
        for i in range(len(chunks)):
            if i == 0:
                overlapped_chunks.append(chunks[i])
            else:
                overlap_text=" ".join(chunks[i-1].split()[-overlap//5:])  # Approximate word count for overlap
                new_chunk=overlap_text + " " + chunks[i]
                overlapped_chunks.append(new_chunk.strip())
        return overlapped_chunks
    return chunks

CHUNKERS={
    "fixed":chunk_fixed,
    "sentence":chunk_sentence
}



