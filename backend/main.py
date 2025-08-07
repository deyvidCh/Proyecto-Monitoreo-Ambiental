from fastapi import FastAPI
import serial
import json
import time

app = FastAPI(title="Sistema de Monitoreo Ambiental", version="1.0.0")

ARDUINO_PORT = "COM3"  
BAUDRATE = 9600

def leer_arduino():
    try:
        with serial.Serial(ARDUINO_PORT, BAUDRATE, timeout=1) as ser:
            linea = ser.readline().decode('utf-8').strip()
            if linea.startswith("{") and linea.endswith("}"):
                return json.loads(linea)
    except Exception as e:
        print(f"Error al leer Arduino: {e}")
    return {
        "temperature": None,
        "humidity": None,
        "air_quality": None,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "ipv6_address": ""
    }

@app.get("/")
async def root():
    return {"message": "Sistema de Monitoreo Ambiental - Backend API"}

@app.get("/api/data")
async def get_data():
    data = leer_arduino()
    data["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    return data
