import socket
import json

HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Puerto de escucha

print(f"--- SERVIDOR ESCUCHANDO EN {HOST}:{PORT} ---")

# Crear el socket servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    
    while True:
        # Esperar conexión del Flet
        conn, addr = s.accept()
        with conn:
            # Recibimos los datos
            data = conn.recv(4096)
            if data:
                try:
                    # Convertimos de bytes a texto y luego a Diccionario
                    mensaje = json.loads(data.decode('utf-8'))
                    
                    print(f"\n[Recibido desde Flet]:")
                    print(f" > Acelerómetro X: {mensaje.get('acc_x')}")
                    print(f" > Temperatura:    {mensaje.get('temp')}")
                    print(f" > Datos crudos:   {mensaje}")
                except json.JSONDecodeError:
                    print("Error al decodificar JSON")