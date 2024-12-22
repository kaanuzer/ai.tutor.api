# main.py

import uvicorn
from fastapi import FastAPI
from application.controllers.chat_controller import router as chat_router

app = FastAPI(title="Clean Architecture + Event-Driven Chat Example")
app.include_router(chat_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)