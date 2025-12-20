"""Invoice Activities - PDF processing and FastAPI integration."""
import base64
from dataclasses import dataclass
import httpx
from temporalio import activity
from config.settings import get_settings


@dataclass
class UploadResult:
    """Result of invoice upload to FastAPI."""
    success: bool
    filename: str
    message: str
    invoice_id: str | None = None


@activity.defn
async def upload_invoice_to_api(filename: str, content: bytes) -> UploadResult:
    """
    Upload PDF invoice to FastAPI service.

    Args:
        filename: Original filename of the PDF.
        content: PDF file content as bytes.

    Returns:
        UploadResult with status and details.
    """
    settings = get_settings()
    # FIXED: Správny endpoint je /invoice (nie /api/v1/invoice/upload)
    url = f"{settings.fastapi_url}/invoice"

    activity.logger.info(f"Uploading {filename} to {url}...")

    # FIXED: FastAPI očakáva JSON s base64, nie multipart
    file_b64 = base64.b64encode(content).decode("utf-8")

    payload = {
        "file_b64": file_b64,
        "filename": filename
    }

    headers = {
        "X-API-Key": settings.ls_api_key,
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                data = response.json()
                activity.logger.info(f"Upload successful: {filename}")
                return UploadResult(
                    success=True,
                    filename=filename,
                    message=data.get("message", "Upload successful"),
                    invoice_id=str(data.get("invoice_id")) if data.get("invoice_id") else None
                )
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                activity.logger.error(f"Upload failed: {error_msg}")
                return UploadResult(
                    success=False,
                    filename=filename,
                    message=error_msg
                )
        except httpx.RequestError as e:
            error_msg = f"Request error: {str(e)}"
            activity.logger.error(error_msg)
            return UploadResult(
                success=False,
                filename=filename,
                message=error_msg
            )


@activity.defn
async def validate_pdf(content: bytes) -> bool:
    """
    Validate that content is a valid PDF.

    Args:
        content: File content as bytes.

    Returns:
        True if valid PDF.
    """
    # PDF files start with %PDF-
    is_valid = content[:5] == b"%PDF-"

    if is_valid:
        activity.logger.info("PDF validation passed")
    else:
        activity.logger.warning("Invalid PDF: missing %PDF- header")

    return is_valid
