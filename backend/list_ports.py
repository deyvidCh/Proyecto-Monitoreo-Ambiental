import serial.tools.list_ports

def list_available_ports():
    print("Buscando puertos seriales disponibles...")
    print("=" * 50)
    
    ports = serial.tools.list_ports.comports()
    
    if not ports:
        print("No se encontraron puertos seriales.")
        return
    
    print(f"Encontrados {len(ports)} puerto(s):\n")
    
    arduino_ports = []
    
    for i, port in enumerate(ports, 1):
        # Verifica si es un puerto Arduino por palabras clave
        is_arduino = any(keyword in port.description.lower() 
                         for keyword in ['arduino', 'usb serial', 'ch340', 'cp210x'])
        status = "Arduino detectado" if is_arduino else "Puerto genérico"
        
        print(f"{i}. {port.device}")
        print(f"   Descripción: {port.description}")
        print(f"   Hardware ID: {port.hwid}")
        print(f"   Estado: {status}\n")
        
        if is_arduino:
            arduino_ports.append(port.device)
    
    print("=" * 50)
    
    if arduino_ports:
        print(f"Puertos Arduino detectados: {arduino_ports}")
        print("El sistema usará automáticamente el primer puerto Arduino encontrado.")
    else:
        print("No se detectaron puertos Arduino específicos.")
        print("El sistema intentará usar el primer puerto disponible.")
    
    print("\nPara usar un puerto específico, edita MANUAL_PORT en main.py.")

if __name__ == "__main__":
    list_available_ports()
