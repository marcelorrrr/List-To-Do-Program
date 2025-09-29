# app.py

from flask import Flask, jsonify, request, render_template
import services

app = Flask(__name__)

@app.route('/')
def home():
    """
    Esta ruta sirve nuestro archivo principal index.html.
    """
    return render_template('index.html')


@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    tareas = services.obtener_todas()
    return jsonify([tarea.to_dict() for tarea in tareas])

@app.route('/tareas', methods=['POST'])
def crear_nueva_tarea():
    datos = request.json
    titulo = datos.get('titulo')
    descripcion = datos.get('descripcion')
    if not titulo:
        return jsonify({"error": "El título es obligatorio"}), 400
    
    nueva_tarea = services.crear(titulo, descripcion)
    return jsonify(nueva_tarea.to_dict()), 201

@app.route('/tareas/<int:tarea_id>', methods=['GET'])
def obtener_tarea(tarea_id):
    tarea = services.obtener_por_id(tarea_id)
    if tarea:
        return jsonify(tarea.to_dict())
    return jsonify({"error": "Tarea no encontrada"}), 404

@app.route('/tareas/<int:tarea_id>', methods=['PUT'])
def actualizar_tarea_endpoint(tarea_id):
    tarea = services.obtener_por_id(tarea_id)
    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404
    
    datos = request.json
    titulo = datos.get('titulo', tarea.titulo)
    descripcion = datos.get('descripcion', tarea.descripcion)
    completada = datos.get('completada', tarea.completada)
    
    tarea_actualizada = services.actualizar(tarea_id, titulo, descripcion, completada)
    return jsonify(tarea_actualizada.to_dict())

@app.route('/tareas/<int:tarea_id>', methods=['DELETE'])
def eliminar_tarea_endpoint(tarea_id):
    tarea = services.obtener_por_id(tarea_id)
    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404
    
    services.eliminar(tarea_id)
    return jsonify({"mensaje": "Tarea eliminada exitosamente"}), 200

if __name__ == '__main__':
    from database import create_table
    create_table()
    app.run(debug=True)