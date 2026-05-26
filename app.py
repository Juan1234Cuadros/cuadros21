from flask import Flask, jsonify, request
from datetime import datetime
import json
import os

app = Flask(__name__)

# Archivo de persistencia en Apache
JSON_FILE = '/var/www/html/peritajes.json'

# Inicializar el archivo con tus motos base
if not os.path.exists(JSON_FILE):
    motos_base = [
        {"placa": "XYZ-123", "marca": "Yamaha", "modelo": "FZ25", "estado": "En revisión", "falla": "Frenos"},
        {"placa": "ABC-987", "marca": "Suzuki", "modelo": "Gixxer 250", "estado": "Espera de repuestos", "falla": "Cambio de pastillas"},
        {"placa": "JDC21H", "marca": "Bajaj", "modelo": "Pulsar NS200", "estado": "Registrado para peritaje", "falla": "Revisión general"}
    ]
    with open(JSON_FILE, 'w') as f:
        json.dump(motos_base, f, indent=4)

# 1. GET GENERAL
@app.route('/api/registros', methods=['GET'])
def get_registros():
    try:
        with open(JSON_FILE, 'r') as f:
            inventario = json.load(f)
    except Exception:
        inventario = []
    return jsonify({
        "hora_servidor": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "inventario": inventario,
        "servidor": "Servidor-Cuadros-Backend"
    }), 200

# 2. POST (Para registrar por si acaso)
@app.route('/api/peritajes', methods=['POST'])
def save_peritaje():
    data = request.get_json()
    if not data or 'placa' not in data:
        return jsonify({"error": "Falta la placa"}), 400
    try:
        with open(JSON_FILE, 'r') as f:
            peritajes = json.load(f)
    except Exception:
        peritajes = []
    peritajes.append({"placa": data['placa'], "marca": "Custom", "modelo": "Moto", "estado": "Revision", "falla": "Chequeo"})
    with open(JSON_FILE, 'w') as f:
        json.dump(peritajes, f, indent=4)
    return jsonify({"mensaje": "Peritaje guardado exitosamente"}), 201

# 3. DELETE DINÁMICO (El paso 1 de la guía del profe)
@app.route('/api/peritajes/<string:placa_id>', methods=['DELETE'])
def delete_peritaje(placa_id):
    try:
        with open(JSON_FILE, 'r') as f:
            peritajes = json.load(f)
    except Exception:
        return jsonify({"error": "No hay peritajes"}), 404
        
    moto_a_remover = None
    for moto in peritajes:
        if moto.get('placa') == placa_id:
            moto_a_remover = moto
            break
            
    if not moto_a_remover:
        return jsonify({"error": f"Vehículo {placa_id} no encontrado"}), 404
        
    nuevos_peritajes = [m for m in peritajes if m.get('placa') != placa_id]
    
    with open(JSON_FILE, 'w') as f:
        json.dump(nuevos_peritajes, f, indent=4)
        
    return jsonify({
        "message": f"Vehículo {placa_id} entregado al cliente con éxito",
        "moto_removida": moto_a_remover
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# --- NUEVA FUNCIONALIDAD: Inventario (A medio hacer) ---
@app.route('/api/inventario', methods=['GET'])
def get_inventario():
    return jsonify({"mensaje": "Módulo de inventario en construcción..."})