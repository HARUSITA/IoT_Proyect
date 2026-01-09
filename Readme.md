# 🌐 IoT_Proyect - Sistema de Monitoreo Inteligente

¡Bienvenido a **IoT_Proyect**! Este es un sistema de Internet de las Cosas diseñado para capturar datos del entorno y enviarlos a la nube para su visualización y análisis en tiempo real.

---

## 🚀 Características
* **Conectividad Wi-Fi:** Conexión automática a redes locales.
* **Lectura de Sensores:** Captura de datos analógicos y digitales.
* **Transmisión de Datos:** Soporta protocolos [HTTP / MQTT].
* **Alertas Visuales:** Feedback mediante indicadores LED en la placa.
* **Escalabilidad:** Fácil de añadir nuevos sensores o actuadores.

## 🛠️ Hardware Requerido
| Componente | Cantidad | Descripción |
| :--- | :---: | :--- |
| **Microcontrolador** | 1 | ESP32 o NodeMCU (ESP8266) |
| **Sensores** | - | [Ej: DHT11, MQ-135, LDR] |
| **Actuadores** | - | [Ej: Relay de 5V, LEDs, Buzzer] |
| **Cables** | - | Jumpers Macho-Hembra y Macho-Macho |
| **Alimentación** | 1 | Cable Micro USB de datos |

## 🔌 Diagrama de Conexión (Referencia)
Aquí tienes una guía rápida de cómo conectar los componentes básicos:

| Componente | Pin Sensor | Pin Microcontrolador |
| :--- | :--- | :--- |
| Sensor VCC | VCC / 5V | 3.3V o 5V |
| Sensor GND | GND | GND |
| Datos Sensor | DATA / OUT | GPIO 4 (D4) |
| LED / Relay | IN | GPIO 2 (D2) |

---

## 💻 Requisitos de Software
1.  **Arduino IDE** (Versión 2.0 o superior recomendada).
2.  **Gestor de Placas:** Soporte para ESP32 o ESP8266 instalado.
3.  **Librerías Necesarias:**
    * `WiFi.h`
    * `PubSubClient` (Si usas MQTT)
    * [Añade otras librerías específicas aquí]

---

## 🔧 Instalación y Puesta en Marcha

### 1. Clonar el repositorio
Copia el proyecto a tu máquina local:
```bash
git clone [https://github.com/HARUSITA/IoT_Proyect.git](https://github.com/HARUSITA/IoT_Proyect.git)
