import serial
from fastapi import FastAPI

app = FastAPI(title="Sistema de Monitoreo Ambiental", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Sistema de Monitoreo Ambiental - Backend API"}
