
// Establece el comportamiento de expandir y colapsar el widget del clima.
const widget = document.getElementById('widget');
widget.addEventListener('click', (event)=> {
    event.stopPropagation(); 
    widget.classList.toggle('colapsado');
    widget.classList.toggle('expandido');
});

// Establece el comportamiento de colapsar el widget al hacer clic en cualquier parte de la pagina web.
document.addEventListener('click', (event) => {
    if(widget.classList.contains('expandido')) {
        widget.classList.toggle('colapsado');
        widget.classList.toggle('expandido');
    };
});
