# 🛵 IoT_Proyect: Control de Acceso Vehicular (ESCOM)

Este proyecto es una solución integral de **Internet de las Cosas (IoT)** diseñada para automatizar y asegurar el acceso de motocicletas a las instalaciones de **ESCOM**. Combina un sistema de gestión web robusto con tecnología de reconocimiento automático de placas (**ANPR**) para optimizar el flujo vehicular.

## 📑 Tabla de Contenidos
* [Arquitectura del Sistema](#-arquitectura-del-sistema)
* [Componentes de Hardware](#-componentes-de-hardware)
* [Stack Tecnológico](#-stack-tecnológico)
* [Instalación y Configuración](#-instalación-y-configuración)
* [Flujo de Operación](#-flujo-de-operación)
* [Documentación y Recursos](#-documentación-y-recursos)
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

```

### 4. Implementación IoT

1. Configura tu **Raspberry Pi** para actuar como broker MQTT (ej. usando Mosquitto).
2. Carga el código en el **ESP32** asegurándote de que apunte a la dirección IP de la Raspberry Pi para la publicación y suscripción de datos.

---

## 🔄 Flujo de Operación

1. **Registro:** El alumno inscribe su motocicleta en la plataforma web asociada a su perfil.
2. **Detección:** Al acercarse al acceso, el sistema **ANPR** detecta y lee la placa de la motocicleta.
3. **Comunicación:** El **ESP32** envía la placa detectada a la Raspberry Pi vía **MQTT**.
4. **Validación:** La Raspberry Pi consulta la base de datos **MySQL** para verificar la autorización.
5. **Acceso:** Si la placa está autorizada, se registra el evento (entrada/salida) y el sistema permite el paso.

---

## 📂 Documentación y Recursos
Puedes encontrar el material de apoyo y la presentación detallada en la carpeta `/docs`:

* [Presentación del Proyecto (PPTX)](./docs/IOT2.pptx)
* [Diagramas de Arquitectura](./docs/)

---

## 👥 Autores

* **Morgans** - *Equipo de desarrollo*:
* **EMIR** 
* **HARUMI** 
* **JOSUE** 
* **EMILIA** 

---

> **Nota:** Este proyecto fue desarrollado para la unidad de **Sistemas Embebidos 6CM3**.

```

```
