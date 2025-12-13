import flet as ft
import asyncio
import socket  # <--- NUEVO
import json    # <--- NUEVO

# Configuración de red
HOST = '127.0.0.1'
PORT = 65432

async def main(page: ft.Page):
    page.title = "Simulador de Datos (Empatica E4)"
    page.vertical_alignment = "start"
    page.padding = 20

    configuracion_sensores = [
        {"nombre": "acc_x", "min": 40.0, "max": 70.0, "res": 0.000001, "inicio": 51.976955},
        {"nombre": "acc_y", "min": 10.0, "max": 30.0, "res": 0.000001, "inicio": 14.231976},
        {"nombre": "acc_z", "min": 20.0, "max": 40.0, "res": 0.000001, "inicio": 28.649323},
        {"nombre": "bvp",   "min": -50.0,"max": 50.0, "res": 0.01,     "inicio": 31.610494},
        {"nombre": "eda",   "min": 0.0,  "max": 5.0,  "res": 0.000001, "inicio": 1.068864},
        {"nombre": "temp",  "min": 30.0, "max": 40.0, "res": 0.01,     "inicio": 35.424470}
    ]

    valores = {}

    contenedor = ft.Column(spacing=25)
    page.add(ft.Text("Panel de Control de Sensores", size=22, weight="bold"), contenedor)

    # Actualiza valores de sliders visualmente
    def actualizar_valor(nombre, valor):
        valores[nombre].value = f"{valor:.6f}"
        valores[nombre].update()

    # Crear sliders dinámicos
    for conf in configuracion_sensores:
        valores[conf["nombre"]] = ft.Text(str(conf["inicio"]), size=14)

        slider = ft.Slider(
            min=conf["min"],
            max=conf["max"],
            value=conf["inicio"],
            label="{value}",
            on_change=lambda e, n=conf["nombre"]: actualizar_valor(n, e.control.value),
        )

        contenedor.controls.append(
            ft.Column([
                ft.Row([
                    ft.Text(conf["nombre"], size=16, weight="bold"),
                    valores[conf["nombre"]],
                ], alignment="space_between"), 
                slider
            ])
        )
    
    page.update()

    # ================================
    #  🔥 ENVÍO DE DATOS POR PUERTO 🔥
    # ================================
    async def auto_guardado():
        contador = 0
        while True: 
            try:
                # 1. Recopilar datos
                datos = {n: float(v.value) for n, v in valores.items()}
                
                # 2. Imprimir en consola local (Opcional)
                print(f"Enviando paquete #{contador}...")

                # 3. ENVIAR POR SOCKET
                # Usamos un bloque try/except específico para la red
                # para que si falla la conexión, la app no se cierre.
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(0.5) # No bloquear la UI si el servidor no responde rápido
                        s.connect((HOST, PORT))
                        
                        # Convertir diccionario a JSON string y luego a bytes
                        mensaje_bytes = json.dumps(datos).encode('utf-8')
                        s.sendall(mensaje_bytes)
                        print(" -> Enviado con éxito.")
                
                except ConnectionRefusedError:
                    print(" -> Error: No se encontró el servidor receptor (¿Ejecutaste receptor.py?).")
                except Exception as ex:
                    print(f" -> Error de red: {ex}")

                contador += 1
                await asyncio.sleep(1)   # Esperar 1 segundo

            except Exception as e:
                print(f"Error crítico en loop: {e}")
                break

    asyncio.create_task(auto_guardado())

ft.app(target=main, view=ft.WEB_BROWSER)