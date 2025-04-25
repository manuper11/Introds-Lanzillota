import datetime
from flask import Blueprint, flash, jsonify, request, render_template, url_for, redirect, current_app
import requests

reservasBp = Blueprint("reservasBp", __name__, template_folder='templates')

@reservasBp.route('/', methods=["GET", "POST"])
def reserva():
    habitaciones = get_habitaciones()

    if request.method == "POST":
        habitacion_id = request.form['habitacion_id']
        cantidad_habitaciones = request.form['cantidad_habitaciones']
        cantidad_personas = request.form['cantidad_personas']
        fecha_desde = request.form['fecha_desde']
        fecha_hasta = request.form['fecha_hasta']

        api_ruta = current_app.config['API_ROUTE']
        api_url = f"{api_ruta}reservas/check-disponibilidad"
        params = {
            'habitacionId': habitacion_id,
            'cantidadHabitaciones': cantidad_habitaciones,
            'fechaDesde': fecha_desde,
            'fechaHasta': fecha_hasta
        }
        headers = {'Content-Type': 'application/json'}

        response = requests.get(api_url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data['success'] and data['disponible']:
                habitacion_seleccionada = next((hab for hab in habitaciones if hab['id'] == int(habitacion_id)), None)
                habitacion_nombre = habitacion_seleccionada['nombre'] if habitacion_seleccionada else 'N/A'
                return render_template(
                    "checkout_reserva.html", 
                    fecha_desde=fecha_desde, 
                    fecha_hasta=fecha_hasta, 
                    cantidad_habitaciones=cantidad_habitaciones, 
                    cantidad_personas=cantidad_personas, 
                    habitacion_id=habitacion_id, 
                    habitacion_nombre=habitacion_nombre, 
                    precio_total=data['precioTotal']
                )
            else:
                flash(data.get('message', 'No hay disponibilidad para las fechas seleccionadas'))
        else:
            flash("Error al verificar disponibilidad: " + response.json().get("message", ""))
    
    return render_template("reservas.html", habitaciones=habitaciones)


@reservasBp.route('/checkout', methods=["GET", "POST"])
def checkout_reserva():
    if request.method == "POST":
        data = {
            'email_cliente': request.form['email_cliente'],
            'nombre_cliente': request.form['nombre_cliente'],
            'telefono_cliente': request.form['telefono_cliente'],
            'fecha_desde': request.form['fecha_desde'],
            'fecha_hasta': request.form['fecha_hasta'],
            'cantidad_habitaciones': request.form['cantidad_habitaciones'],
            'cantidad_personas': request.form['cantidad_personas'],
            'metodo_pago': request.form['metodo_pago'],
            'habitacion_id': request.form['habitacion_id'],
            'precio_total': request.form['precio_total']
        }
        api_ruta = current_app.config['API_ROUTE']
        api_url = api_ruta + "reservas"
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(api_url, json=data, headers=headers)
        if response.status_code == 200:
            codigo_reserva = response.json().get("codigo_reserva")
            return render_template('confirmacion_reserva.html', codigo_reserva=codigo_reserva)
        else:
            flash("Error al crear la reserva: " + response.json().get("message", ""))
            return render_template(
                'checkout_reserva.html', 
                fecha_desde=data['fecha_desde'], 
                fecha_hasta=data['fecha_hasta'], 
                cantidad_habitaciones=data['cantidad_habitaciones'], 
                cantidad_personas=data['cantidad_personas'], 
                habitacion_id=data['habitacion_id'], 
                precio_total=data['precio_total']
            )    
    return redirect(url_for('reservasBp.reserva'))

@reservasBp.route('/gestion_reservas')
def gestion_reservas():
    rol = request.cookies.get('rol')
    if rol == 'admin':
        api_ruta = current_app.config['API_ROUTE'] + "reservas"
        response = requests.get(api_ruta)
        if response.status_code == 200:
            reservas = response.json().get("reservas", [])
            reservas_proximas = []
            reservas_activas = []
            reservas_rechazadas = []

            hoy = datetime.date.today()

            for reserva in reservas:
                fecha_desde = datetime.datetime.strptime(reserva['fecha_desde'], '%Y-%m-%d').date()
                fecha_hasta = datetime.datetime.strptime(reserva['fecha_hasta'], '%Y-%m-%d').date()
                
                if reserva['estado'] == 'rechazada':
                    reservas_rechazadas.append(reserva)
                elif fecha_desde > hoy:
                    reservas_proximas.append(reserva)
                elif fecha_desde <= hoy <= fecha_hasta:
                    reservas_activas.append(reserva)
                
            
            reservas_proximas = sorted(reservas_proximas, key=lambda x: datetime.datetime.strptime(x['fecha_desde'], '%Y-%m-%d').date())
            reservas_activas = sorted(reservas_activas, key=lambda x: datetime.datetime.strptime(x['fecha_hasta'], '%Y-%m-%d').date(), reverse=True)

            return render_template(
                'gestion_reservas.html', 
                reservas_proximas=reservas_proximas, 
                reservas_activas=reservas_activas, 
                reservas_rechazadas=reservas_rechazadas
            )
        else:
            return jsonify({"message": "Error al obtener las reservas"}), 500
    return redirect(url_for('adminBp.admin'))

    

@reservasBp.route('/estado_reserva')
def estado_reserva():
    return render_template('estado_reserva.html')

def get_habitaciones():
    try:
        api_ruta = current_app.config['API_ROUTE']
        api_url = api_ruta + "habitaciones/"
        response = requests.get(api_url)
        lista_habitaciones = response.json()
    except requests.exceptions.RequestException as e:
        lista_habitaciones = []
    return lista_habitaciones