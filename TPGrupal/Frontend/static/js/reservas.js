document.addEventListener("DOMContentLoaded", () => {
    const scrollToFormBtn = document.getElementById("scrollToFormBtn");
    const form = document.getElementById("form_reserva");
    const mensajesError = document.getElementById("mensajes_error");

    if (scrollToFormBtn && form) {
        scrollToFormBtn.addEventListener("click", function() {
            form.scrollIntoView({ behavior: "smooth" });
        });
    }

    form.addEventListener("submit", function(event) {
        mensajesError.innerHTML = "";
        const fechaDesde = document.querySelector('input[name="fecha_desde"]').value;
        const fechaHasta = document.querySelector('input[name="fecha_hasta"]').value;
        const habitacionId = document.querySelector('select[name="habitacion_id"]').value;
        const cantidadHabitaciones = document.querySelector('input[name="cantidad_habitaciones"]').value;
        const cantidadPersonas = document.querySelector('input[name="cantidad_personas"]').value;
        const hoy = new Date();

        let errores = [];
        hoy.setHours(0, 0, 0, 0); 

        if (!fechaDesde || !fechaHasta || !habitacionId || !cantidadHabitaciones || !cantidadPersonas) {
            errores.push('Todos los campos son obligatorios');
        }

        if (new Date(fechaHasta) < new Date(fechaDesde)) {
            errores.push("La fecha 'Hasta' no puede ser anterior a la fecha 'Desde'.");
        }

        if (new Date(fechaDesde) < hoy) {
            errores.push("La fecha 'Desde' no puede ser anterior a la fecha de hoy.");
        }

        // Si hay errores, prevenir el envio del formulario
        if (errores.length > 0) {
            event.preventDefault();
            mostrarErrores(errores);
            return;
        }
    });

    function mostrarErrores(errores) {
        mensajesError.innerHTML = "";
        errores.forEach(error => {
            const errorItem = document.createElement("p");
            errorItem.textContent = error;
            mensajesError.appendChild(errorItem);
        });
    }
});