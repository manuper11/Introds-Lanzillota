import config from './config.js';

document.addEventListener('DOMContentLoaded', function () {
    // El contenedor de la lista y los elementos
    const reviewsList = document.getElementById('reviews-list');
    const searchInput = document.getElementById('search-input');
    let reviewsElements = Array.from(document.querySelectorAll('.review-item'));
    // Elementos de la paginacion y fultrado
    const itemsPerPage = 5;
    let currentPage = 1;
    let filteredReviews = reviewsElements;


    const URL = config.apiBaseUrl;

    // Agrega los eventos al reviewsList, quien disparada los eventos si la zona clickeada tiene el targe
    // Me ahorro de poner eventos a todos los botones
    reviewsList.addEventListener('click', function(event) {
        if (event.target.classList.contains('visibility-button')) {
            handleVisibilityButtonClick(event);
        } else if (event.target.classList.contains('estado-button')) {
            handleEstadoButtonClick(event);
        } else if (event.target.classList.contains('delete-button')) {
            handleDeleteButtonClick(event);
        }

    });

    // Evento para la Delete
    function handleDeleteButtonClick(event) {
        const button = event.target;
        const reviewElement = button.closest('.review-item');
        const id = reviewElement.getAttribute('data-id');
        // Mostrar una confirmación antes de proceder con la eliminación
        const confirmation = confirm("¿Posta queres eliminar esta review?");
        if (confirmation) {
            deleteReview(id, reviewElement);
        }
    }

    // Evento para la visibilidad
    function handleVisibilityButtonClick(event) {
        const button = event.target;
        const reviewElement = button.closest('.review-item');
        const id = reviewElement.getAttribute('data-id');
        const visible = reviewElement.getAttribute('data-visible') === 'true';
        updateVisibility(id, visible, button, reviewElement);
    }

    // Evento para para los estados
    function handleEstadoButtonClick(event) {
        const button = event.target;
        const reviewElement = button.closest('.review-item');
        const id = reviewElement.getAttribute('data-id');
        const estado = reviewElement.getAttribute('data-estado');
        updateEstado(id, estado, button, reviewElement);
    }

    // Peticiones a la API y actualizacion de botones 
    function updateVisibility(id, visible, button, reviewElement) {
        fetch(`${URL}/reviews/${id}/visibility`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ visible: !visible })
        })
        .then(response => response.json())
        .then(data => {
            alert("Perfecto. " + data.message);
            reviewElement.setAttribute('data-visible', (!visible).toString());

            //Controlo que no se muestre el boton borrar para Reviews favoritas
            const estado = reviewElement.getAttribute('data-estado');
            const button_delete = reviewElement.querySelector('.delete-button');
            if (visible && estado !== 'favorita') {
                button_delete.classList.remove('d-none');
                button_delete.classList.add('d-block');
            } else {
                button_delete.classList.remove('d-block');
                button_delete.classList.add('d-none');
            }
            updateVisibleButton(button, !visible);
        })
        .catch(error => {
            alert('Error al actualizar la visibilidad');
        });
    }

    function deleteReview(id, reviewElement) {
        fetch(`${URL}/reviews/${id}/delete`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            alert("Perfecto. " + data.message);
            reviewElement.remove(); // Elimina el elemento de la lista
            location.reload(); // Recargar la página después de la eliminación
        })
        .catch(error => {
            alert('Error al eliminar la review');
        });
    }

    function updateEstado(id, estado, button, reviewElement) {
        const newEstado = (estado === 'nueva' || estado === 'favorita') ? 'desmarcada' : 'favorita';
        fetch(`${URL}/reviews/${id}/state`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ estado: newEstado })
        })
        .then(response => response.json())
        .then(data => {
            alert("Estado actualizado: " + data.message);
            reviewElement.setAttribute('data-estado', newEstado);
            button.textContent = newEstado === 'desmarcada' ? 'Marcar como favorita' : 'Quitar de favoritas';
            updateReviewFav(estado, newEstado, reviewElement);
        })
        .catch(error => {
            alert('Error al actualizar el estado');
        });
    }

    // Actualizaciones de botones
    function updateVisibleButton(button, newVisible) {
        button.textContent = newVisible ? 'Ocultar' : 'Mostrar';
        button.className = newVisible ? 'btn btn-danger visibility-button' : 'btn btn-success visibility-button';
    }

    function updateReviewFav(estado, newEstado, reviewElement) {
        const button_delete = reviewElement.querySelector('.delete-button');
        const isVisible = reviewElement.getAttribute('data-visible') === 'true';
        
        reviewElement.classList.toggle('favorite-review', newEstado === 'favorita');
        button_delete.classList.toggle('d-none', newEstado === 'favorita' || isVisible);
        button_delete.classList.toggle('d-block', !(newEstado === 'favorita' || isVisible));
    }
    
    // Filtra y recarga la lista cada vez que se toca un boton de cambio de estado o de siguiente pagina.
    function renderReviews() {
        reviewsList.innerHTML = '';
        const start = (currentPage - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        const reviewsToRender = filteredReviews.slice(start, end);
        reviewsToRender.forEach(review => {
            reviewsList.appendChild(review);
        });
        updatePagination();
    }

    // Agrego eventos al tocar un boton de filtro por estado de reviews
    document.querySelectorAll('.filter-btn').forEach(button => {
        button.addEventListener('click', function () {
            const titulo = document.getElementById('text-list-review');
            titulo.innerText = this.textContent;
            const criterio = this.getAttribute('data-filtro');
            const filter = this.getAttribute(criterio);
            filteredReviews = reviewsElements.filter(review => {
                return filter === 'all' || review.getAttribute(criterio) === filter;
            });
            currentPage = 1;
            renderReviews();
        });
    });

    // Función de búsqueda
    function searchReviews(query) {
        query = query.toLowerCase();
        filteredReviews = reviewsElements.filter(review => {
            const text = review.querySelector('.review-text').textContent.toLowerCase();
            const author = review.querySelector('.blockquote-footer').textContent.toLowerCase();
            return text.includes(query) || author.includes(query);
        });
        currentPage = 1;
        const titulo = document.getElementById('text-list-review');
        titulo.innerText = 'Todas';
        renderReviews();
    }

    searchInput.addEventListener('input', function () {
        searchReviews(this.value);
    });

    // Funciones de paginacion
    function changePage(newPage) {
        if (newPage < 1 || newPage > Math.ceil(filteredReviews.length / itemsPerPage)) return;
        currentPage = newPage;
        renderReviews();
    }

    document.getElementById('prev-page').addEventListener('click', function (e) {
        e.preventDefault();
        changePage(currentPage - 1);
    });

    document.getElementById('next-page').addEventListener('click', function (e) {
        e.preventDefault();
        changePage(currentPage + 1);
    });

    function updatePagination() {
        const totalPages = Math.ceil(filteredReviews.length / itemsPerPage);
        document.querySelector('#prev-page').parentElement.classList.toggle('disabled', currentPage === 1);
        document.querySelector('#next-page').parentElement.classList.toggle('disabled', currentPage === totalPages);
    }

    renderReviews();
});
