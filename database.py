# database.py

import sqlite3

DATABASE_NAME = "tareas.db"

def get_db_connection():
    """Crea y devuelve una conexión a la base de datos."""
    conn = sqlite3.connect(DATABASE_NAME)
    # Permite acceder a las columnas por nombre
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    """Crea la tabla de tareas si no existe."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            completada BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# --- Funciones CRUD ---

def obtener_todas_las_tareas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tareas")
    tareas = cursor.fetchall()
    conn.close()
    return tareas

def crear_tarea(titulo, descripcion):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tareas (titulo, descripcion) VALUES (?, ?)",
                   (titulo, descripcion))
    nuevo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return nuevo_id

def obtener_tarea_por_id(tarea_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tareas WHERE id = ?", (tarea_id,))
    tarea = cursor.fetchone()
    conn.close()
    return tarea

def actualizar_tarea(tarea_id, titulo, descripcion, completada):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tareas 
        SET titulo = ?, descripcion = ?, completada = ?
        WHERE id = ?
    """, (titulo, descripcion, completada, tarea_id))
    conn.commit()
    conn.close()

def eliminar_tarea(tarea_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))
    conn.commit()
    conn.close()