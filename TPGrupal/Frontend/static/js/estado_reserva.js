import config from './config.js';

document.addEventListener("DOMContentLoaded", () => {
    const apiBaseUrl = config.apiBaseUrl;
    const formEstadoReserva = document.getElementById("form_estado_reserva");
    const mensajesError = document.getElementById("mensajes_error");
    const resultadoReservaElement = document.getElementById("resultado_reserva");
    const contadorDiasRestantesElement = document.getElementById("contador_dias_restantes");
    const diasRestantesElement = document.getElementById("dias_restantes");

    if (formEstadoReserva) {
        formEstadoReserva.addEventListener("submit", function(event) {
            event.preventDefault(); // Prevenir el envío del formulario

            const codigoReserva = document.querySelector('input[name="codigo_reserva"]').value;

            if (!codigoReserva) {
                mostrarErrores(['Por favor, ingrese un código de reserva válido.']);
                return;
            }

            const urlConsultaReserva = new URL(`${apiBaseUrl}/reservas/`);
            urlConsultaReserva.searchParams.append('codigo_reserva', codigoReserva);

            // Realizar la consulta del estado de la reserva
            fetch(urlConsultaReserva, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success && data.reservas.length > 0) {
                    const reserva = data.reservas[0];
                    mostrarResultadoReserva(reserva);
                } else {
                    mostrarErrores(['No se encontró ninguna reserva con ese código.']);
                }
            })
            .catch(error => {
                mostrarErrores(['Error de red al consultar la reserva.']);
            });
        });

        function mostrarErrores(errores) {
            mensajesError.innerHTML = ""; // Clear previous errors
            errores.forEach(error => {
                const errorItem = document.createElement("p");
                errorItem.textContent = error;
                mensajesError.appendChild(errorItem);
            });
        }

        function mostrarResultadoReserva(reserva) {
            resultadoReservaElement.style.display = 'block';
            contadorDiasRestantesElement.style.display = 'block';
            document.getElementById("email_cliente").textContent = reserva.email_cliente;
            document.getElementById("nombre_cliente").textContent = reserva.nombre_cliente;
            document.getElementById("telefono_cliente").textContent = reserva.telefono_cliente;
            document.getElementById("fecha_desde").textContent = formatearFecha(reserva.fecha_desde);
            document.getElementById("fecha_hasta").textContent = formatearFecha(reserva.fecha_hasta);
            document.getElementById("cantidad_habitaciones").textContent = reserva.cantidad_habitaciones;
            document.getElementById("cantidad_personas").textContent = reserva.cantidad_personas;
            document.getElementById("metodo_pago").textContent = reserva.metodo_pago;
            document.getElementById("estado").textContent = reserva.estado;
            document.getElementById("precio_total").textContent = reserva.precio_total;
            document.getElementById("tipo_habitacion").textContent = reserva.tipo_habitacion;

            const diasRestantes = calcularDiasRestantes(reserva.fecha_desde);
            if (reserva.estado === 'rechazada') {
                diasRestantesElement.textContent = 'Lamentablemente su reserva ha sido rechazada. Por favor, póngase en contacto con nosotros para más información.';
            } else {
                if (diasRestantes > 0) {
                    diasRestantesElement.textContent = `¡Faltan ${diasRestantes} días para que comience su estadía!`;
                } else if (diasRestantes === 0) {
                    diasRestantesElement.textContent = '¡Su estadía comienza hoy!';
                } else {
                    diasRestantesElement.textContent = 'Su estadía ya ha comenzado.';
                }
            }



            // Scroll al bloque de resultados
            resultadoReservaElement.scrollIntoView({ behavior: 'smooth' });
        }
    

        function formatearFecha(fecha) {
            const [year, month, day] = fecha.split('-');
            return `${day}/${month}/${year}`;
        }

        function calcularDiasRestantes(fecha_desde) {
            const fechaActual = new Date();
            const fechaInicio = new Date(fecha_desde);
            const diferenciaTiempo = fechaInicio - fechaActual;
            const diferenciaDias = Math.ceil(diferenciaTiempo / (1000 * 3600 * 24));
            return diferenciaDias;
        }
    }
});