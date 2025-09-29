import psycopg2
import os # Para leer la URL de la base de datos

# Obtenemos la URL de la variable de entorno que configuraremos en Render
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    """Crea y devuelve una conexión a la base de datos PostgreSQL."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def create_table():
    """Crea la tabla de tareas si no existe."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # La sintaxis de PostgreSQL es ligeramente diferente (SERIAL para autoincremento)
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

# --- Funciones CRUD (Necesitan pequeños ajustes) ---

def obtener_todas_las_tareas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, descripcion, completada FROM tareas ORDER BY id ASC")
    # Convertimos las tuplas a diccionarios para que sea más fácil de usar
    tareas = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return tareas

def crear_tarea(titulo, descripcion):
    conn = get_db_connection()
    cursor = conn.cursor()
    # RETURNING id nos devuelve el ID de la nueva fila creada
    cursor.execute("INSERT INTO tareas (titulo, descripcion) VALUES (%s, %s) RETURNING id",
                   (titulo, descripcion))
    nuevo_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return nuevo_id


#falta corregir

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