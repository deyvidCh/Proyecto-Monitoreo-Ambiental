import serial
from fastapi import FastAPI

app = FastAPI(title="Sistema de Monitoreo Ambiental", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Sistema de Monitoreo Ambiental - Backend API"}

@app.get("/api/data")
async def get_data():
    # Valores simulados
    data = {
        "temperature": 25.0,
        "humidity": 65.0,
        "air_quality": 350,
        "timestamp": "2025-08-06T15:30:00",
        "ipv6_address": "fe80::1234:abcd:5678:9abc"
    }
    return data
