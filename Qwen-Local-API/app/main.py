from fastapi import FastAPI

from app.routers.chat import router as chat_router

app = FastAPI(title="Qwen Local API")


@app.get("/")
def root():
    return {"message": "Qwen Local API is running"}


app.include_router(chat_router)