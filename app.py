import uuid
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Voice Setu API",
    description="Video upload and translation API prototype",
    version="0.1.0",
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

ALLOWED_TYPES = {
    "video/mp4",
    "video/mpeg",
    "video/quicktime",
    "video/webm",
}


class TranslateRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    source_language: str = "hi"
    target_language: str = "en"


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Voice Setu API is working",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api")
def api_info():
    return {
        "name": "Voice Setu API",
        "features": [
            "video upload",
            "translation endpoint prototype",
        ],
        "voice_cloning": "not implemented yet",
        "video_dubbing": "not implemented yet",
        "docs": "/docs",
    }


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Please upload an MP4, MPEG, MOV, or WebM video.",
        )

    original_name = Path(file.filename or "video.mp4").name
    extension = Path(original_name).suffix.lower()

    if not extension:
        extension = (
            ".mp4" if file.content_type == "video/mp4"
            else ".video"
        )

    filename = f"{uuid.uuid4().hex}{extension}"
    file_path = UPLOAD_DIR / filename
    size = 0

    try:
        with file_path.open("wb") as buffer:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break

                size += len(chunk)

                if size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="Video must be 100 MB or smaller.",
                    )

                buffer.write(chunk)

    except Exception:
        file_path.unlink(missing_ok=True)
        raise

    finally:
        await file.close()

    return {
        "success": True,
        "message": "Video uploaded successfully.",
        "filename": filename,
        "size_bytes": size,
    }


@app.post("/translate")
def translate_text(request: TranslateRequest):
    raise HTTPException(
        status_code=501,
        detail=(
            "Translation engine is not connected yet. "
            "Add a translation model to enable this endpoint."
        ),
    )
