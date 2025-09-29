# models.py

class Tarea:
    """
    Representa el modelo de una Tarea.
    """
    def __init__(self, id, titulo, descripcion, completada=False):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.completada = completada

    def to_dict(self):
        """
        Convierte el objeto Tarea a un diccionario para poder enviarlo como JSON.
        """
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "completada": self.completada
        }