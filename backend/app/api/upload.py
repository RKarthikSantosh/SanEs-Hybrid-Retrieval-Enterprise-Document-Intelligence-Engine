from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.embeddings.text_embeddings import embed_text
from app.loaders.pdf_loader import extract_pdf_pages
from app.retrieval.chroma_store import store_chunks

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf" and not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)

    file_path = raw_dir / file.filename
    contents = await file.read()
    file_path.write_bytes(contents)

    pages, page_count = extract_pdf_pages(file_path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    chunks = []
    chunk_id = 1
    for page_number, page_text in enumerate(pages, start=1):
        for chunk_text in splitter.split_text(page_text):
            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "text": chunk_text,
                    "page": page_number,
                    "filename": file.filename,
                    "embedding": embed_text(chunk_text),
                }
            )
            chunk_id += 1

    store_chunks(chunks)

    return {
        "filename": file.filename,
        "pages": page_count,
        "text_length": sum(len(page_text) for page_text in pages),
        "chunks": chunks,
    }