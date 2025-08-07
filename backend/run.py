"""
Script de ejecución para el backend del Sistema de Monitoreo Ambiental
"""

import uvicorn
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app

if __name__ == "__main__":
    print("Iniciando Sistema de Monitoreo Ambiental...")
    print("Backend FastAPI disponible en: http://localhost:8000")
    print("WebSocket disponible en: ws://localhost:8000/ws")
    print("Documentación API: http://localhost:8000/docs")
    print("")
    print("IMPORTANTE: Verificar que el Arduino esté conectado")
    print("y que el puerto serial esté correctamente configurado en main.py")
    print("=" * 50)
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info"
    )
