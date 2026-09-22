document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('modal-producto');
    const modalNombre = document.getElementById('modal-nombre');
    const modalDescripcion = document.getElementById('modal-descripcion');
    const reproductorAudio = document.getElementById('reproductor-audio');
    const audioSource = document.getElementById('audio-source');
    const contenedorAudio = document.getElementById('contenedor-audio');
    const btnCerrar = document.getElementById('btn-cerrar-modal');

    const imgIzq = document.getElementById('img-modal-izq');
    const imgDer = document.getElementById('img-modal-der');

    document.querySelectorAll('.tarjeta-producto').forEach(tarjeta => {
        tarjeta.addEventListener('click', (e) => {

            if (e.target.tagName === 'BUTTON' && !e.target.classList.contains('btn-detalles')) {
                return;
            }

            const nombre = tarjeta.dataset.nombre;
            const descripcion = tarjeta.dataset.descripcion;
            const estilo = tarjeta.dataset.estilo;
            const audioUrl = tarjeta.dataset.audio;
            const imagenUrl = tarjeta.dataset.imagen; 
            const imagenIzqUrl = tarjeta.dataset.imagenIzq;
            const imagenDerUrl = tarjeta.dataset.imagenDer;

            modalNombre.textContent = nombre;
            modalDescripcion.textContent = descripcion;

            modal.setAttribute('data-tema', estilo || 'default');

            if (imagenUrl) {
                modal.style.setProperty('--bg-imagen', `url('${imagenUrl}')`);
            } else {
                modal.style.setProperty('--bg-imagen', 'none');
            }

            if (imgIzq) {
                if (imagenIzqUrl) {
                    imgIzq.src = imagenIzqUrl;
                    imgIzq.parentElement.style.display = 'block';
                } else {
                    imgIzq.parentElement.style.display = 'none';
                }
            }

            if (imgDer) {
                if (imagenDerUrl) {
                    imgDer.src = imagenDerUrl;
                    imgDer.parentElement.style.display = 'block';
                } else {
                    imgDer.parentElement.style.display = 'none';
                }
            }

    
            if (audioUrl) {
                audioSource.src = audioUrl;
                reproductorAudio.load();
                contenedorAudio.style.display = 'block';
            } else {
                contenedorAudio.style.display = 'none';
                reproductorAudio.pause();
            }

            modal.showModal();
        });
    });

    const cerrarModal = () => {
        reproductorAudio.pause();
        reproductorAudio.currentTime = 0;
        modal.close();
    };

    btnCerrar.addEventListener('click', cerrarModal);

    modal.addEventListener('click', (e) => {
        const rect = modal.getBoundingClientRect();
        const isInDialog = (rect.top <= e.clientY && e.clientY <= rect.top + rect.height &&
            rect.left <= e.clientX && e.clientX <= rect.left + rect.width);
        if (!isInDialog) {
            cerrarModal();
        }
    });

    const botonesEliminar = document.querySelectorAll('.boton-peligro');
    botonesEliminar.forEach(boton => {
        boton.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Estás seguro de que deseas eliminar este producto?');
            if (!confirmacion) {
                e.preventDefault(); 
            }
        });
    });
});