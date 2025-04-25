document.addEventListener("DOMContentLoaded", function() {
    // Scrollear al formulario de checkout al cargar la página
    document.getElementById("checkout-form").scrollIntoView({ behavior: "smooth" });

    const form = document.getElementById("form_checkout");
    const mensajesError = document.getElementById("mensajes_error");

    form.addEventListener("submit", function(event) {
        mensajesError.innerHTML = ""; 
        const email = document.querySelector('input[name="email_cliente"]').value;
        const nombre = document.querySelector('input[name="nombre_cliente"]').value;
        const telefono = document.querySelector('input[name="telefono_cliente"]').value;
        const metodoPago = document.querySelector('select[name="metodo_pago"]').value;

        let errores = [];

        const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        if (!emailPattern.test(email)) {
            errores.push("El email no tiene un formato válido.");
        }

        if (nombre.trim() === "") {
            errores.push("El nombre es obligatorio.");
        }

        if (metodoPago === "") {
            errores.push("Seleccione un método de pago.");
        }

        // Si hay errores, prevenir el envio del formulario
        if (errores.length > 0) {
            event.preventDefault();
            mostrarErrores(errores);
        }
    });

    function mostrarErrores(errores) {
        errores.forEach(error => {
            const errorItem = document.createElement("p");
            errorItem.textContent = error;
            errorItem.classList.add("text-danger");
            mensajesError.appendChild(errorItem);
        });
    }
});