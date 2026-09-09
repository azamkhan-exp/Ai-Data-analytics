import os
from fastapi import HTTPException

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

def validate_uploaded_file(filename: str, content_length: int) -> str:
    """
    Validates file extension and size. Returns the lowercase extension.
    """
    if not filename:
        raise HTTPException(status_code=400, detail="Filename missing from upload request.")

    ext = filename.lower().split('.')[-1]
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '.{ext}'. Supported formats: {', '.join('.' + e for e in sorted(ALLOWED_EXTENSIONS))}."
        )

    if content_length == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty (0 bytes).")

    if content_length > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds the 50MB size limit (received {round(content_length / (1024*1024), 2)} MB)."
        )

    return ext
