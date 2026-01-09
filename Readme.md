# 🛵 IoT_Proyect: Control de Acceso Vehicular (ESCOM)

Este proyecto es una solución integral de **Internet de las Cosas (IoT)** diseñada para automatizar y asegurar el acceso de motocicletas a las instalaciones de **ESCOM**. Combina un sistema de gestión web robusto con tecnología de reconocimiento automático de placas (**ANPR**) para optimizar el flujo vehicular.

## 📑 Tabla de Contenidos
* [Arquitectura del Sistema](#-arquitectura-del-sistema)
* [Componentes de Hardware](#-componentes-de-hardware)
* [Stack Tecnológico](#-stack-tecnológico)
* [Instalación y Configuración](#-instalación-y-configuración)
* [Flujo de Operación](#-flujo-de-operación)
* [Autores](#-autores)

---

## 🏗️ Arquitectura del Sistema
El sistema se divide en tres niveles operativos:

1.  **Capa Administrativa (Web):** Interfaz para el registro de alumnos y vinculación de sus vehículos.
2.  **Capa de Procesamiento (Raspberry Pi):** Servidor central que gestiona el broker **MQTT** y valida los accesos consultando la base de datos.
3.  **Capa de Control (ESP32):** Nodo sensor que captura eventos y actúa como efector inteligente en el punto de acceso físico.

---

## 🛠️ Componentes de Hardware
* **Raspberry Pi:** Actúa como el "cerebro" central y broker de mensajes.
* **ESP32:** Microcontrolador encargado de la comunicación en el punto de acceso.
* **Cámara de Alta Resolución:** Utilizada para la captura de imágenes de las placas.
* **Módulo ANPR/OCR:** Algoritmo de reconocimiento de caracteres para procesar la placa detectada.

---

## 💻 Stack Tecnológico
* **Backend:** Node.js
* **Base de Datos:** MySQL (Gestionada vía XAMPP)
* **Comunicación:** Protocolo MQTT para mensajería asíncrona entre dispositivos.
* **Entorno:** Node.js v22+

---

## 🔧 Instalación y Configuración

### 1. Requisitos Previos
Asegúrate de tener instalados los siguientes programas:
* [XAMPP](https://www.apachefriends.org/es/index.html) (con servicio MySQL activo).
* [Node.js](https://nodejs.org/) (versión 22 o superior).

### 2. Configuración de la Base de Datos
1.  Abre el panel de control de **XAMPP** e inicia el módulo **MySQL**.
2.  Accede a `phpMyAdmin`.
3.  Crea una nueva base de datos e importa el archivo `database.sql` incluido en este repositorio para generar la estructura de alumnos y vehículos.

### 3. Configuración del Servidor Web
Clona el repositorio e instala las dependencias:

```bash
# Clonar el proyecto
git clone [https://github.com/HARUSITA/IoT_Proyect.git](https://github.com/HARUSITA/IoT_Proyect.git)

# Entrar al directorio
cd IoT_Proyect

# Instalar dependencias
npm install

# Iniciar el servidor
node app.js
