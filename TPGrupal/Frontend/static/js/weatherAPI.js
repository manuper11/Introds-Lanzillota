
// Funcion que aplica el icono correspondiente al estado del clima.
function cambiar_Icono(elemento, estado_clima) {
    fetch('/weather_icons')
    .then(response => response.json())
    .then(data => {
        switch (estado_clima) {
            case 'clouds':
                elemento.src = data.clouds;
                break;
            case 'sunny':
                elemento.src = data.sunny;
                break;
            case 'rain':
                elemento.src = data.rain;
                break;
            case 'snow':
                elemento.src = data.snow;
                break;
            
            default:
                elemento.src = 'static/imgs/dia-nublado.jpg';
        };
    });
};

// Captura los datos del back-end de app.py y los muestra en el html.
fetch('/clima_actual')
    .then(response => response.json())
    .then(data => {

        const widget_temperatura = document.getElementById('temperatura');
        widget_temperatura.innerText = data.temperatura + 'ºC';

        const widget_ciudad = document.getElementById('ciudad');
        widget_ciudad.innerText = data.ciudad;

        const widget_humedad = document.getElementById('humedad');
        widget_humedad.innerText = data.humedad + ' %';
        
        const widget_viento = document.getElementById('velocidad_viento');
        widget_viento.innerText = data.velocidad_viento + ' km/h';

        const widget_temperatura_min = document.getElementById('temperatura_minima_hoy');
        widget_temperatura_min.innerText = data.temperatura_minima + 'º';

        const widget_temperatura_max = document.getElementById('temperatura_maxima_hoy');
        widget_temperatura_max.innerText = data.temperatura_maxima + 'º';

        const widget_estado = document.getElementById('clima_actual_icon');
        cambiar_Icono(widget_estado, data.estado.toLowerCase());
    });

fetch('/pronostico_clima')
    .then(response => response.json())
    .then(data => {

        const dias = Object.keys(data);

        for (let i = 0; i < dias.length; i++) {
            const dia = dias[i];

            const widget_dia = document.getElementById(`dia_${i + 1}`);
            widget_dia.innerText = dia;

            const widget_temperatura_min = document.getElementById(`temperatura_minima_${i + 1}`);
            widget_temperatura_min.innerText = data[dia].temperatura_minima + 'º';

            const widget_temperatura_max = document.getElementById(`temperatura_maxima_${i + 1}`);
            widget_temperatura_max.innerText = data[dia].temperatura_maxima + 'º';

            const widget_estado = document.getElementById(`forecast_icon_${i + 1}`);
            cambiar_Icono(widget_estado, data[dia].estado.toLowerCase());
        };
    });

