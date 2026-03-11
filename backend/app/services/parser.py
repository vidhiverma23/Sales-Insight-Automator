"""File parsing service: CSV/XLSX → structured text for LLM consumption."""

import io
import pandas as pd
from fastapi import UploadFile, HTTPException


ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}


async def parse_file(file: UploadFile, max_size_mb: int = 10) -> str:
    """
    Parse an uploaded CSV or XLSX file into a text summary suitable for LLM input.
    
    Returns a structured text representation including:
    - Column names and types
    - Statistical summary
    - First 50 rows of data
    """
    # Validate extension
    filename = file.filename or ""
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Read file content
    content = await file.read()

    # Validate size
    size_mb = len(content) / (1024 * 1024)
    if size_mb > max_size_mb:
        raise HTTPException(
            status_code=400,
            detail=f"File too large ({size_mb:.1f} MB). Maximum: {max_size_mb} MB"
        )

    # Parse into DataFrame
    try:
        if ext == ".csv":
            df = pd.read_csv(io.BytesIO(content))
        else:
            df = pd.read_excel(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")

    if df.empty:
        raise HTTPException(status_code=400, detail="The uploaded file contains no data.")

    # Build structured text representation
    lines = [
        f"## Dataset Overview",
        f"- **Filename**: {filename}",
        f"- **Rows**: {len(df):,}",
        f"- **Columns**: {len(df.columns)}",
        "",
        "## Column Information",
        df.dtypes.to_string(),
        "",
        "## Statistical Summary",
        df.describe(include="all").to_string(),
        "",
        "## Sample Data (first 50 rows)",
        df.head(50).to_string(index=False),
    ]

    return "\n".join(lines)
