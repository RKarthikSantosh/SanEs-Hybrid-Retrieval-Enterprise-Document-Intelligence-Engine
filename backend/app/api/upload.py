from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.loaders.pdf_loader import extract_pdf_text

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

    text, page_count = extract_pdf_text(file_path)

    return {
        "filename": file.filename,
        "pages": page_count,
        "text_length": len(text),
    }