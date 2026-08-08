from pathlib import Path

import fitz


def extract_pdf_text(file_path: Path) -> tuple[str, int]:
    document = fitz.open(file_path)
    try:
        text = "\n".join(page.get_text() for page in document)
        return text, document.page_count
    finally:
        document.close()