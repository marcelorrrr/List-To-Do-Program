// Espera a que todo el contenido del HTML se cargue antes de ejecutar el script
document.addEventListener('DOMContentLoaded', () => {

    // --- Referencias a los elementos del HTML ---
    const formulario = document.getElementById('formulario-tarea');
    const tituloInput = document.getElementById('titulo-tarea');
    const descripcionInput = document.getElementById('descripcion-tarea');
    const listaTareas = document.getElementById('lista-tareas');

    // --- URL de nuestra API ---
const API_URL = '/tareas';

    // --- FUNCIÓN PARA OBTENER Y MOSTRAR TODAS LAS TAREAS ---
    async function obtenerYMostrarTareas() {
        try {
            const respuesta = await fetch(API_URL);
            const tareas = await respuesta.json();

            // Limpiar la lista actual
            listaTareas.innerHTML = '';

            // Crear y añadir cada tarea a la lista en el HTML
            tareas.forEach(tarea => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <span class="tarea ${tarea.completada ? 'completada' : ''}">
                        <strong>${tarea.titulo}</strong>: ${tarea.descripcion || ''}
                    </span>
                    <div class="acciones">
                        <button class="completar" data-id="${tarea.id}">✔️</button>
                        <button class="eliminar" data-id="${tarea.id}">❌</button>
                    </div>
                `;
                listaTareas.appendChild(li);
            });

        } catch (error) {
            console.error("Error al obtener las tareas:", error);
        }
    }

    // --- FUNCIÓN PARA AGREGAR UNA NUEVA TAREA ---
    async function agregarTarea(event) {
        event.preventDefault(); // Evita que el formulario recargue la página

        const titulo = tituloInput.value;
        const descripcion = descripcionInput.value;

        if (!titulo) {
            alert("El título es obligatorio.");
            return;
        }

        try {
            await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ titulo, descripcion }),
            });

            // Limpiar el formulario y refrescar la lista
            formulario.reset();
            obtenerYMostrarTareas();

        } catch (error) {
            console.error("Error al agregar la tarea:", error);
        }
    }

    // --- FUNCIÓN PARA MANEJAR ACCIONES (COMPLETAR/ELIMINAR) ---
    async function manejarAccionesTareas(event) {
        const id = event.target.dataset.id;
        
        // Eliminar Tarea
        if (event.target.classList.contains('eliminar')) {
            try {
                await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
                obtenerYMostrarTareas();
            } catch (error) {
                console.error("Error al eliminar la tarea:", error);
            }
        }

        // Completar/Descompletar Tarea
        if (event.target.classList.contains('completar')) {
            try {
                // Primero obtenemos el estado actual de la tarea
                const respuesta = await fetch(`${API_URL}/${id}`);
                const tarea = await respuesta.json();
                
                // Enviamos la petición PUT con el estado invertido
                await fetch(`${API_URL}/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ completada: !tarea.completada }),
                });
                obtenerYMostrarTareas();
            } catch (error) {
                console.error("Error al actualizar la tarea:", error);
            }
        }
    }

    // --- EVENT LISTENERS ---
    formulario.addEventListener('submit', agregarTarea);
    listaTareas.addEventListener('click', manejarAccionesTareas);

    // --- CARGA INICIAL DE DATOS ---
    obtenerYMostrarTareas();
});