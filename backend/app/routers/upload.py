"""Upload router: handles file upload, AI summary generation, and email delivery."""

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Request
from pydantic import EmailStr
from email_validator import validate_email, EmailNotValidError

from app.security import limiter, verify_api_key
from app.config import get_settings
from app.services.parser import parse_file
from app.services.ai_engine import generate_summary
from app.services.mailer import send_summary_email

router = APIRouter(prefix="/api", tags=["Upload & Analysis"])


@router.post(
    "/upload",
    summary="Upload sales data and send AI summary via email",
    description=(
        "Accepts a `.csv` or `.xlsx` file along with a recipient email address. "
        "The file is parsed, analyzed by an AI engine (Google Gemini), and the "
        "resulting professional sales brief is emailed to the recipient."
    ),
    response_description="Confirmation with email delivery status",
    dependencies=[Depends(verify_api_key)],
)
@limiter.limit("5/minute")
async def upload_and_analyze(
    request: Request,
    file: UploadFile = File(..., description="Sales data file (.csv or .xlsx)"),
    email: str = Form(..., description="Recipient email address"),
):
    """
    End-to-end flow:
    1. Validate the file type and size
    2. Parse the file into structured text
    3. Generate an AI-powered executive summary
    4. Email the summary to the provided address
    """
    # Validate email format
    try:
        validation = validate_email(email, check_deliverability=False)
        email = validation.normalized
    except EmailNotValidError as e:
        raise HTTPException(status_code=400, detail=f"Invalid email address: {str(e)}")

    settings = get_settings()

    # Step 1 & 2: Parse the file
    data_text = await parse_file(file, max_size_mb=settings.MAX_FILE_SIZE_MB)

    # Step 3: Generate AI summary
    try:
        summary_html = await generate_summary(data_text)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI summary generation failed: {str(e)}"
        )

    # Step 4: Send email
    try:
        email_response = await send_summary_email(
            to_email=email,
            summary_html=summary_html,
            filename=file.filename or "sales_data",
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Email delivery failed: {str(e)}"
        )

    return {
        "status": "success",
        "message": f"Sales insight report sent to {email}",
        "details": {
            "filename": file.filename,
            "recipient": email,
            "email_id": email_response.get("id") if isinstance(email_response, dict) else str(email_response),
        },
    }


@router.get(
    "/health",
    summary="Health check",
    description="Returns the application health status.",
    tags=["System"],
)
async def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy", "service": "Sales Insight Automator"}
