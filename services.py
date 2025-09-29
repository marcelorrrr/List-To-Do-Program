# services.py
import database
from models import Tarea

def obtener_todas():
    tareas_db = database.obtener_todas_las_tareas()
    return [Tarea(id=t['id'], titulo=t['titulo'], descripcion=t['descripcion'], completada=t['completada']) for t in tareas_db]

def obtener_por_id(tarea_id):
    tarea_db = database.obtener_tarea_por_id(tarea_id)
    if tarea_db:
        return Tarea(id=tarea_db['id'], titulo=tarea_db['titulo'], descripcion=tarea_db['descripcion'], completada=tarea_db['completada'])
    return None

def crear(titulo, descripcion):
    nuevo_id = database.crear_tarea(titulo, descripcion)
    return obtener_por_id(nuevo_id)

def actualizar(tarea_id, titulo, descripcion, completada):
    database.actualizar_tarea(tarea_id, titulo, descripcion, completada)
    return obtener_por_id(tarea_id)

def eliminar(tarea_id):
    database.eliminar_tarea(tarea_id)