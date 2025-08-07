from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import serial
import json
import time
import threading
import asyncio
import socket
import ipaddress

app = FastAPI(title="Sistema de Monitoreo Ambiental", version="1.0.0")

ARDUINO_PORT = "COM3"  
BAUDRATE = 9600

def leer_arduino():
    try:
        with serial.Serial(ARDUINO_PORT, BAUDRATE, timeout=1) as ser:
            linea = ser.readline().decode('utf-8').strip()
            print(f"[DEBUG] Recibido desde Arduino: {linea}")  # <-- Agrega este print
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

def get_local_ipv6_address():
    try:
        hostname = socket.gethostname()
        addrinfo = socket.getaddrinfo(hostname, None, socket.AF_INET6)
        for addr_info in addrinfo:
            ipv6_addr = addr_info[4][0]
            try:
                ipaddress.IPv6Address(ipv6_addr)
                if ipv6_addr.startswith('fe80::'):
                    return ipv6_addr
            except ipaddress.AddressValueError:
                continue
        for addr_info in addrinfo:
            ipv6_addr = addr_info[4][0]
            try:
                ipaddress.IPv6Address(ipv6_addr)
                return ipv6_addr
            except ipaddress.AddressValueError:
                continue
        return "::1"
    except Exception as e:
        print(f"Error obteniendo IPv6 local: {e}")
        return "fe80::1a2b:3c4d:5e6f:7890"


def leer_arduino_en_hilo():
    global ultimo_dato
    ipv6 = get_local_ipv6_address()
    while True:
        dato = leer_arduino()
        dato["ipv6_address"] = ipv6  
        ultimo_dato = dato

        for client in connected_clients.copy():
            try:
                if dato["temperature"] is not None:
                    asyncio.run(client.send_text(json.dumps(dato)))
            except Exception as e:
                print(f"[WARN] Cliente desconectado o error de envío: {e}")
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
