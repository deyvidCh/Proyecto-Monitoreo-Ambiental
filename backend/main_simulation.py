from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import time
from datetime import datetime
import threading
import random

app = FastAPI(title="Sistema de Monitoreo Ambiental (Simulación)", version="1.0.0")

connected_clients = []
sim_data = {
    "temperature": 25.0,
    "humidity": 55.0,
    "air_quality": 400,
    "timestamp": "",
    "ipv6_address": ""
}
is_running = False

def simular_datos():
    global sim_data
    while is_running:
        sim_data = {
            "temperature": round(random.uniform(20, 30), 1),
            "humidity": round(random.uniform(40, 80), 1),
            "air_quality": random.randint(100, 900),
            "timestamp": datetime.now().isoformat(),
            "ipv6_address": "fe80::1a2b:3c4d:1234:5678"
        }
        for client in connected_clients.copy():
            try:
                import asyncio
                asyncio.run(client.send_text(json.dumps(sim_data)))
            except Exception:
                connected_clients.remove(client)
        time.sleep(1)

@app.get("/")
async def root():
    return {"message": "Sistema de Monitoreo Ambiental - Simulación"}

@app.get("/api/data")
async def get_data():
    return sim_data

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
def iniciar_hilo_simulacion():
    global is_running
    is_running = True
    hilo = threading.Thread(target=simular_datos, daemon=True)
    hilo.start()
