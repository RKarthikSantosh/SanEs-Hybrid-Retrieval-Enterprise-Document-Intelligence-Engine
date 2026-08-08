from pathlib import Path

import fitz


def extract_pdf_pages(file_path: Path) -> tuple[list[str], int]:
    document = fitz.open(file_path)
    try:
        pages = [page.get_text() for page in document]
        return pages, document.page_count
    finally:
        document.close()