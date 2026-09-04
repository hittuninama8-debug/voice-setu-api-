UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Voice Setu API is working"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):

    allowed_types = [
        "video/mp4",
        "video/mpeg",
        "video/quicktime",
        "video/webm"
    ]

    if file.content_type not in allowed_types:
        return {
            "success": False,
            "message": "Please upload a video file."
        }

    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            buffer.write(chunk)

    return {
        "success": True,
        "message": "Video uploaded successfully.",
        "filename": filename
    }
    
