from fastapi import FastAPI

app = FastAPI()

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
