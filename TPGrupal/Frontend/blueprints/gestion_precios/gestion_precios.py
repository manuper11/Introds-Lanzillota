from flask import Blueprint, jsonify, request, render_template, url_for, redirect, current_app
import requests

#Blueprint 
gestionPreciosBp = Blueprint("gestionPreciosBp", __name__, template_folder='templates')

@gestionPreciosBp.route('/', methods = ['GET'])
def pedir_precios_habitaciones():
    rol = request.cookies.get('rol')
    if rol == 'admin':
        api_ruta = current_app.config['API_ROUTE']
        api_url = api_ruta + "habitaciones/"
        try:                       
            response = requests.get(api_url)
            if response.status_code == 200:
                datos = response.json()
                return render_template('gestion_precios.html', datos=datos)
            else:
                return jsonify({"message": "Error al cargar las habitaciones"}), 500
        except requests.RequestException:
            return jsonify({"message": "Error al cargar las habitaciones"}), 500
    return redirect(url_for('adminBp.admin'))
    

@gestionPreciosBp.route('/', methods=['POST'])
def modificar_precios_habitaciones():
    id_habitacion = request.form['id']
    nuevo_precio = str(request.form['precio_noche'])
    api_ruta = current_app.config['API_ROUTE']
    api_url = api_ruta + "gestion_precios/gestion_precios"
                 
    try:
        response = requests.patch(api_url, json={'id': id_habitacion, 'precio_noche': nuevo_precio})

        if response.status_code == 200:
            return redirect(url_for('gestionPreciosBp.pedir_precios_habitaciones', _external=True)) 
        else:
            return jsonify({"message": "Error al actualizar el precio"}), 500
    except requests.RequestException:
        return jsonify({"message": "Error al actualizar el precio"}), 500
