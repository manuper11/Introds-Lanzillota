import config from './config.js';

document.addEventListener("DOMContentLoaded", () => {
    const apiBaseUrl = config.apiBaseUrl;

    // Inicializar DataTables (usando jquery)
    $('#proximasTable').DataTable({
        "paging": true,
        "searching": true,
        "ordering": false,
        "info": true,
        "lengthChange": true,
        "pageLength": 10,
        "language": {
            "search": "Buscar:",
            "lengthMenu": "Mostrar _MENU_ registros por página",
            "zeroRecords": "No se encontraron resultados",
            "info": "Mostrando página _PAGE_ de _PAGES_",
            "infoEmpty": "No hay registros disponibles",
            "infoFiltered": "(filtrado de _MAX_ registros totales)",
            "paginate": {
                "first": "Primero",
                "last": "Último",
                "next": "Siguiente",
                "previous": "Anterior"
            }
        }
    });

    $('#rechazadasTable').DataTable({
        "paging": true,
        "searching": true,
        "ordering": false,
        "info": true,
        "lengthChange": true,
        "pageLength": 10,
        "language": {
            "search": "Buscar:",
            "lengthMenu": "Mostrar _MENU_ registros por página",
            "zeroRecords": "No se encontraron resultados",
            "info": "Mostrando página _PAGE_ de _PAGES_",
            "infoEmpty": "No hay registros disponibles",
            "infoFiltered": "(filtrado de _MAX_ registros totales)",
            "paginate": {
                "first": "Primero",
                "last": "Último",
                "next": "Siguiente",
                "previous": "Anterior"
            }
        }
    });

    $('#activasTable').DataTable({
        "paging": true,
        "searching": true,
        "ordering": false,
        "info": true,
        "lengthChange": true,
        "pageLength": 10,
        "language": {
            "search": "Buscar:",
            "lengthMenu": "Mostrar _MENU_ registros por página",
            "zeroRecords": "No se encontraron resultados",
            "info": "Mostrando página _PAGE_ de _PAGES_",
            "infoEmpty": "No hay registros disponibles",
            "infoFiltered": "(filtrado de _MAX_ registros totales)",
            "paginate": {
                "first": "Primero",
                "last": "Último",
                "next": "Siguiente",
                "previous": "Anterior"
            }
        }
    });

    $('#cancelarReservaModal').on('show.bs.modal', function(event) {
        const button = $(event.relatedTarget);
        const reservaId = button.data('id');
        const modal = $(this);
        modal.find('#reservaId').val(reservaId);
    });

    $('#informacionContactoModal').on('show.bs.modal', function(event) {
        const button = $(event.relatedTarget);
        const email = button.data('email');
        const telefono = button.data('telefono');
        const modal = $(this);
        modal.find('#contactoEmail').text(email);
        modal.find('#contactoTelefono').text(telefono);
    });

    // Ajustamos las fechas para mostrarlas en el formato dd/mm/yyyy
    const formatDate = (dateStr) => {
        const [year, month, day] = dateStr.split('-');
        return `${day}/${month}/${year}`;
    };
    
    document.querySelectorAll('.fecha').forEach((cell) => {
        cell.textContent = formatDate(cell.textContent);
    });

    document.getElementById("contenedor-reservas").scrollIntoView({ behavior: "smooth" });


    const cancelarReservaForm = document.getElementById('cancelarReservaForm');
    cancelarReservaForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const reservaId = document.getElementById('reservaId').value;
        const motivoRechazo = document.getElementById('motivoRechazo').value;
        const urlUpdateReserva = new URL(`${apiBaseUrl}/reservas/${reservaId}/update`);

        fetch(urlUpdateReserva, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                estado: 'rechazada',
                motivo_rechazo: motivoRechazo
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload(); // Recargar la página para actualizar la lista de reservas
            } else {
                alert('Error al cancelar la reserva: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al cancelar la reserva.');
        });
    });
});