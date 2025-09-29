# database.py
import psycopg2
import os
from psycopg2.extras import DictCursor # Para obtener filas como diccionarios

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    """Crea y devuelve una conexión a la base de datos PostgreSQL."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def create_table():
    """Crea la tabla de tareas si no existe."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id SERIAL PRIMARY KEY,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            completada BOOLEAN NOT NULL DEFAULT FALSE
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# --- Funciones CRUD Completas y Corregidas ---

def obtener_todas_las_tareas():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=DictCursor) # Usa DictCursor
    cursor.execute("SELECT * FROM tareas ORDER BY id ASC")
    tareas = cursor.fetchall()
    cursor.close()
    conn.close()
    return tareas

def crear_tarea(titulo, descripcion):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tareas (titulo, descripcion) VALUES (%s, %s) RETURNING id",
                   (titulo, descripcion))
    nuevo_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return nuevo_id

def obtener_tarea_por_id(tarea_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=DictCursor) # Usa DictCursor
    cursor.execute("SELECT * FROM tareas WHERE id = %s", (tarea_id,))
    tarea = cursor.fetchone()
    cursor.close()
    conn.close()
    return tarea

def actualizar_tarea(tarea_id, titulo, descripcion, completada):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tareas
        SET titulo = %s, descripcion = %s, completada = %s
        WHERE id = %s
    """, (titulo, descripcion, completada, tarea_id))
    conn.commit()
    cursor.close()
    conn.close()

def eliminar_tarea(tarea_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tareas WHERE id = %s", (tarea_id,))
    conn.commit()
    cursor.close()
    conn.close()