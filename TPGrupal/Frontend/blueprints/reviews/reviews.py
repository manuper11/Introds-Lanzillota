from flask import Blueprint, render_template, current_app, redirect, request, flash, url_for
from datetime import datetime
import requests

# Crear el blueprint
reviewsBp = Blueprint('reviewsBp', __name__)

@reviewsBp.route('/', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        api_rute = current_app.config['API_ROUTE']
        codigo_reserva = request.form.get('codigo_reserva')
        nombre_autor = request.form.get('nombre_autor')
        texto = request.form.get('texto')

        # Validaciones para el form
        if not codigo_reserva or not nombre_autor or not texto:
            flash('Todos los campos son obligatorios.', 'warning')
            return redirect(url_for('reviewsBp.reviews') + '#Agregar-review')
        
        try:
            api_url = api_rute + "reservas?codigo_reserva=" + codigo_reserva
            response = requests.get(api_url)
            response.raise_for_status()
            reservas = response.json()
            
            reserva_encontrada = None
            for reserva in reservas['reservas']:
                if reserva['codigo_reserva'] == codigo_reserva:
                    reserva_encontrada = reserva
                    break
            if not reserva_encontrada:
                flash('Código de reserva no válido.', 'warning')
                return redirect(url_for('reviewsBp.reviews') + '#Agregar-review')
            
            # Convertir la fecha de la reserva a un objeto de fecha
            fecha_hasta_str = reserva_encontrada['fecha_hasta']
            fecha_hasta = datetime.strptime(fecha_hasta_str, "%Y-%m-%d").date()

            # Obtener la fecha actual como un objeto de fecha
            fecha_actual = datetime.now().date()

            if fecha_actual <= fecha_hasta:
                flash('No se puede agregar una review antes de la fecha de salida.', 'warning')
                return redirect(url_for('reviewsBp.reviews') + '#Agregar-review')
        except requests.RequestException as e:
            error_message = "Error al obtener datos de la reserva."
            if e.response is not None:
                try:
                    error_message += f" {e.response.json().get('message', '')}"
                except ValueError:
                    error_message += f" {e.response.text}"
            else:
                error_message += f" {str(e)}"
            flash(error_message, 'danger')
            return redirect(url_for('reviewsBp.reviews') + '#Agregar-review')

        # Crear la review
        review = {
            'nombre_autor': nombre_autor,
            'texto': texto,
            'reserva_id': reserva_encontrada['id']
        }
        try:
            api_url = api_rute + "reviews"
            headers = {'Content-Type': 'application/json'}
            response = requests.post(api_url, json=review, headers=headers)
            response.raise_for_status()
            flash('Review agregada exitosamente.', 'success')
            return redirect(url_for('reviewsBp.reviews') + '#Agregar-review')
        except requests.RequestException as e:
            error_message = "Error al agregar la review."
            if e.response is not None:
                try:
                    error_message += f" {e.response.json().get('message', '')}"
                except ValueError:
                    error_message += f" {e.response.text}"
            else:
                error_message += f" {str(e)}"
            flash(error_message, 'danger')
            return redirect(url_for('reviewsBp.reviews') + '#Agregar-review')

    # GET request
    reviews_favs = get_random_reviews()
    return render_template('reviews.html', reviews=reviews_favs)


#Le pido 7 reviews al azar, principalmente las favoritas, sino cualquiera visible.
def get_random_reviews(limit=7):
    try:
        api_ruta = current_app.config['API_ROUTE']
        api_url = api_ruta + "reviews/visible"
        response = requests.get(api_url)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        reviews = response.json()

        # Filtra las reseñas favoritas y las comunes para mostrar
        favorite_reviews = [review for review in reviews if review['estado'] == 'favorita']
        other_reviews = [review for review in reviews if review['estado'] != 'favorita']

        # Selecciona reseñas favoritas al azar
        if len(favorite_reviews) >= limit:
            selected_reviews = random.sample(favorite_reviews, limit)
        else:
            # Asegurar de que hay suficientes reseñas en 'other_reviews' antes de tomar una muestra
            if len(other_reviews) >= (limit - len(favorite_reviews)):
                selected_reviews = favorite_reviews + random.sample(other_reviews, limit - len(favorite_reviews))
            else:
                # Si no hay suficientes reseñas, simplemente devuelve las favoritas y lo que haya en 'other_reviews'
                selected_reviews = favorite_reviews + other_reviews
        
        return selected_reviews
    except requests.RequestException as e:
        print(f"Error fetching reviews: {e}")
        return []

