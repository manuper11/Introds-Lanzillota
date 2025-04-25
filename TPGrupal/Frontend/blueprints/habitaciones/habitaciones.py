from flask import Blueprint,current_app,request, render_template
import requests
habitacionesBp = Blueprint("habitacionesBp", __name__)

@habitacionesBp.route('/', methods=['GET'])
def habitaciones():
    lista_habitaciones = get_habitaciones()
    return render_template('habitaciones.html', habitaciones = lista_habitaciones)

@habitacionesBp.route('/<id>', methods = ['GET'])
def habitaciones_id(id):
    lista_habitaciones = get_habitaciones()
    habitacion = {}
    id = int(id)
    for hab in lista_habitaciones:
        if hab['id'] == id:
            habitacion = hab
            break
    return render_template('habitacion.html', habitacion=habitacion)

def get_habitaciones():
    try:
        api_ruta = current_app.config['API_ROUTE']
        api_url = api_ruta + "habitaciones/"
        response = requests.get(api_url)
        lista_habitaciones = response.json()
    except requests.exceptions.RequestException as e:
        lista_habitaciones = []
    return lista_habitaciones