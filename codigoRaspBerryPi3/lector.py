import cv2
import pytesseract
import serial
import time
import re
import json
import tkinter as tk
from tkinter import font, messagebox
import threading

# --- CONFIGURACION ---
PUERTO_SERIAL = '/dev/ttyUSB0' 
BAUD_RATE = 115200

# Colores ESCOM
COLOR_BLUE = "#004767"
COLOR_BG = "#f4f7f9"
COLOR_WHITE = "#ffffff"

try:
    ser = serial.Serial(PUERTO_SERIAL, BAUD_RATE, timeout=5)
    print("✅ Conectado al ESP32")
except:
    print("❌ Error: Conecta el ESP32 por USB")
    ser = None

# Variables Globales
ultimo_envio = 0
COOLDOWN = 5.0 
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

# --- COMUNICACION ---
def enviar_placa(placa):
    global ultimo_envio
    if not ser:
        print(f"Simulacion envio: {placa}")
        return

    print(f"📡 Enviando: {placa}")
    ser.reset_input_buffer()
    ser.write((placa + "\n").encode('utf-8'))
    threading.Thread(target=leer_respuesta_esp32).start()

def leer_respuesta_esp32():
    global ultimo_envio
    try:
        time.sleep(0.5) 
        if ser and ser.in_waiting:
            linea = ser.readline().decode('utf-8').strip()
            if linea:
                print(f"📩 Recibido: {linea}")
                try:
                    datos = json.loads(linea)
                    # Usamos after para actualizar la GUI sin errores de hilos
                    if datos.get("status") == "autorizado":
                        app_instance.window.after(0, lambda: mostrar_popup_acceso(datos))
                        ultimo_envio = time.time()
                    elif datos.get("status") == "espera":
                         print("⏳ Espere 30s para registrar salida")
                    else:
                        print("⛔ Denegado")
                except: pass
    except Exception as e:
        print(f"Error Serial: {e}")

# --- VENTANA EMERGENTE (ESTILO AZUL ESCOM) ---
def mostrar_popup_acceso(datos):
    popup = tk.Toplevel()
    popup.title("Estado de Acceso")
    popup.geometry("600x350")
    popup.configure(bg=COLOR_BG)
    
    # Header Azul
    header = tk.Frame(popup, bg=COLOR_BLUE, height=60)
    header.pack(fill="x")
    tk.Label(header, text="SISTEMA DE ACCESO", font=("Arial", 14, "bold"), fg="white", bg=COLOR_BLUE).pack(pady=10)

    # Lógica Entrada/Salida
    tipo = datos.get('tipo', 'ACCESO')
    color_texto = "#2ecc71" if tipo == 'ENTRADA' else "#e74c3c"
    icono = "✅ ENTRADA AUTORIZADA" if tipo == 'ENTRADA' else "👋 SALIDA REGISTRADA"
    
    tk.Label(popup, text=icono, font=("Arial", 20, "bold"), fg=color_texto, bg=COLOR_BG).pack(pady=20)
    
    # Datos del Alumno
    f_dato = font.Font(family="Arial", size=14)
    tk.Label(popup, text=f"Nombre: {datos['nombre']}", font=f_dato, bg=COLOR_BG).pack(pady=5)
    tk.Label(popup, text=f"Carrera: {datos['carrera']}", font=f_dato, bg=COLOR_BG).pack(pady=5)
    tk.Label(popup, text=f"Vehiculo: {datos['vehiculo']}", font=f_dato, fg="#666", bg=COLOR_BG).pack(pady=5)
    
    # Cerrar en 5 segundos
    popup.after(5000, popup.destroy)

# --- INTERFAZ PRINCIPAL ---
class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("500x300") # Más compacta
        self.window.configure(bg=COLOR_BLUE)

        # Header Principal
        self.lbl_header = tk.Label(window, text="CONTROL ESCOM", font=("Arial", 20, "bold"), bg=COLOR_BLUE, fg="white")
        self.lbl_header.pack(pady=20)
        
        tk.Label(window, text="(Cámara activa en ventana externa)", font=("Arial", 10), bg=COLOR_BLUE, fg="#ccc").pack()

        # Panel de Registro Manual
        self.manual_frame = tk.Frame(window, bg=COLOR_BG, padx=20, pady=20)
        self.manual_frame.pack(fill="x", padx=20, pady=20)
        
        self.lbl_instruccion = tk.Label(self.manual_frame, text="Placa Manual:", font=("Arial", 12), bg=COLOR_BG)
        self.lbl_instruccion.pack(side="left")
        
        self.entry_placa = tk.Entry(self.manual_frame, font=("Arial", 14), width=12)
        self.entry_placa.pack(side="left", padx=10)
        
        self.btn_enviar = tk.Button(self.manual_frame, text="REGISTRAR", font=("Arial", 10, "bold"), bg=COLOR_BLUE, fg="white", command=self.enviar_manual)
        self.btn_enviar.pack(side="left")

        # Iniciar Camara
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)
        self.cap.set(4, 480)
        self.delay = 15
        self.frame_count = 0
        
        global app_instance
        app_instance = self

        self.update()
        self.window.mainloop()

    def enviar_manual(self):
        texto = self.entry_placa.get().upper().strip()
        if len(texto) >= 5:
            enviar_placa(texto)
            self.entry_placa.delete(0, 'end')
        else:
            messagebox.showwarning("Error", "Mínimo 5 caracteres")

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            self.frame_count += 1
            
            # Procesamiento OCR (Cada 10 cuadros)
            if self.frame_count % 10 == 0 and (time.time() - ultimo_envio) > COOLDOWN:
                cv2.rectangle(frame, (100, 150), (540, 330), (0, 255, 0), 2)
                
                roi = frame[150:330, 100:540]
                gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                _, binaria = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                procesada = cv2.bitwise_not(cv2.morphologyEx(binaria, cv2.MORPH_CLOSE, kernel))
                
                config = r'--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                texto = pytesseract.image_to_string(procesada, config=config)
                placa_ocr = re.sub(r'[^A-Z0-9]', '', texto.upper())

                if 5 <= len(placa_ocr) <= 7:
                    enviar_placa(placa_ocr)

            # MOSTRAR CAMARA USANDO OPENCV (Evita el error de PIL)
            cv2.imshow('Camara ESCOM (Q para salir)', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.window.destroy()
        else:
            self.window.after(self.delay, self.update)

if __name__ == "__main__":
    App(tk.Tk(), "Sistema ESCOM")