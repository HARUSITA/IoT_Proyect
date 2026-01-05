from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# CONFIGURACION BD
db_config = {
    'host': 'localhost', 'user': 'root', 'password': 'mumur05', 'database': 'sistema_escom'
}

def obtener_conexion():
    try: return mysql.connector.connect(**db_config)
    except: return None

@app.route('/verificar', methods=['POST'])
def verificar():
    data = request.json if request.is_json else request.form
    placa = data.get('placa', '').strip()
    
    conn = obtener_conexion()
    if not conn: return jsonify({"status": "error"}), 500
    cursor = conn.cursor(dictionary=True)

    # 1. BUSCAR USUARIO
    query = """
        SELECT a.nombre, a.carrera, v.marca_modelo 
        FROM vehiculos v 
        JOIN alumnos a ON v.alumno_id = a.id 
        WHERE v.placas = %s
    """
    cursor.execute(query, (placa,))
    usuario = cursor.fetchone()

    if usuario:
        # 2. LOGICA ENTRADA / SALIDA CON TIEMPO DE ESPERA
        cursor.execute("SELECT tipo, fecha_hora FROM historial WHERE placa = %s ORDER BY id DESC LIMIT 1", (placa,))
        ultimo = cursor.fetchone()

        nuevo_tipo = 'ENTRADA' # Por defecto

        if ultimo:
            # Calcular tiempo transcurrido en segundos
            tiempo_transcurrido = (datetime.now() - ultimo['fecha_hora']).total_seconds()
            
            if ultimo['tipo'] == 'ENTRADA':
                # Si fue entrada, verificamos que hayan pasado 30 segundos
                if tiempo_transcurrido < 30:
                    cursor.close(); conn.close()
                    print(f"IGNORADO: {placa} (Esperando 30s para salida)")
                    return jsonify({"status": "espera", "msg": "Espere para salir"}), 200
                
                nuevo_tipo = 'SALIDA'
        
        # 3. GUARDAR HISTORIAL
        try:
            cursor.execute("INSERT INTO historial (placa, alumno_nombre, tipo) VALUES (%s, %s, %s)", 
                           (placa, usuario['nombre'], nuevo_tipo))
            conn.commit()
            print(f"REGISTRO {nuevo_tipo}: {usuario['nombre']}")
        except Exception as e:
            print(f"Error BD: {e}")

        cursor.close(); conn.close()
        
        return jsonify({
            "status": "autorizado",
            "tipo": nuevo_tipo,
            "nombre": usuario['nombre'],
            "carrera": usuario['carrera'],
            "vehiculo": usuario['marca_modelo']
        }), 200
    else:
        cursor.close(); conn.close()
        print(f"NO REGISTRADO: {placa}")
        return jsonify({"status": "denegado"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)