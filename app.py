from fastapi import FastAPI

app = FastAPI(title="Voice Setu API")


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Voice Setu API is working"
    }


@app.get("/health")
def health():
    return {"status": "ok"}
