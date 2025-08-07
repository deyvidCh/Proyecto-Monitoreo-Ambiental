from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import serial
import json
import time
import threading
import asyncio 

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

connected_clients = []

def leer_arduino_en_hilo():
    global ultimo_dato
    while True:
        dato = leer_arduino()
        ultimo_dato = dato
        for client in connected_clients.copy():
            try:
                if dato["temperature"] is not None:
                    asyncio.run(client.send_text(json.dumps(dato)))
            except Exception:
                connected_clients.remove(client)
        time.sleep(1)

ultimo_dato = {
    "temperature": None,
    "humidity": None,
    "air_quality": None,
    "timestamp": "",
    "ipv6_address": ""
}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

@app.on_event("startup")
def iniciar_hilo_arduino():
    hilo = threading.Thread(target=leer_arduino_en_hilo, daemon=True)
    hilo.start()
