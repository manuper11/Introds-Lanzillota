from flask import Blueprint, jsonify, url_for
import requests
import datetime

weatherBp = Blueprint("weatherBp", __name__)

"""
    Constantes esenciales para la construcción de la URL de la API del clima.
"""
API_KEY = "dbec3add72c6ecd469b009ae31e34fb5"
LATITUD = "-54.804316946849376"
LONGITUD = "-68.35705777103327"
UNIDAD = "metric"

"""
    Método que se encarga de la comunicación con el servicio de Open Weather y se obtiene
    el pronósitico de la fecha actual.
    Se filtra los datos extra y se toman los útiles.
    Retorna un json response válida para enviar al cliente o navegador.
"""
@weatherBp.route('/clima_actual')
def obtener_clima_actual():
    url = "https://api.openweathermap.org/data/2.5/weather?"
    parametros = {
        'lat': LATITUD,
        'lon': LONGITUD,
        'appid': API_KEY,
        'units': UNIDAD,
    }
    current_response = requests.get(url, params=parametros)
    data = current_response.json()

    temperatura_actual = float(data['main']['temp'])
    temperatura_minima = float(data['main']['temp_min'])
    temperatura_maxima = float(data['main']['temp_max'])
    velocidad_viento = data['wind']['speed']
    humedad = data['main']['humidity']
    ciudad = data['name']
    estado = data['weather'][0]['main']

    current_weather = {
        'temperatura': round(temperatura_actual),
        'temperatura_minima': round(temperatura_minima),
        'temperatura_maxima': round(temperatura_maxima),
        'velocidad_viento': velocidad_viento,
        'humedad': humedad,
        'ciudad': ciudad,
        'estado': estado    
    }
    return jsonify(current_weather)

"""
    Método que se encarga de la comunicación con el servicio de Open Weather con los datos requeridos.
    Se Obtiene el pronóstico de los siguiente cuatro días.
    Se filtra los datos extra y se toman los útiles.
    Retorna un json response válida para enviar al cliente o navegador.
"""
@weatherBp.route('/pronostico_clima')
def obtener_pronostico():
    url = "https://api.openweathermap.org/data/2.5/forecast?" + "cnt=40"
    parametros = {
        'lat': LATITUD,
        'lon': LONGITUD,
        'appid': API_KEY,
        'units': UNIDAD,
    }
    forecast_response = requests.get(url, params=parametros)
    forecast_data = forecast_response.json()
    forecast_weather = {}
    for i in range (8, 40, 8):
        fecha_iso = forecast_data['list'][i]['dt_txt']
        fecha_formateada = datetime.datetime.strptime(fecha_iso, "%Y-%m-%d %H:%M:%S")
        dias_español = ["Lun", "Mar", "Miér", "Jue", "Vier", "Sáb", "Dom"]
        dia = dias_español[fecha_formateada.weekday()]

        temperatura_minima = float(forecast_data['list'][i]['main']['temp_min'])
        temperatura_maxima = float(forecast_data['list'][i]['main']['temp_max'])
        forecast_weather[dia] = {
            'temperatura_minima': round(temperatura_minima),
            'temperatura_maxima': round(temperatura_maxima),
            'estado': forecast_data['list'][i]['weather'][0]['main']
        }
    return jsonify(forecast_weather)

"""
    Método que se encarga de generar la url de los íconos del clima.
"""
@weatherBp.route('/weather_icons')
def iconos():
    iconos = {
        'clouds': url_for('static', filename='imgs/dia-nublado.jpg', _external=True),
        'sunny': url_for('static', filename='imgs/soleado.jpg', _external=True),
        'rain': url_for('static', filename='imgs/lluvioso.jpg', _external=True),
        'snow': url_for('static', filename='imgs/nevado.jpg', _external=True),
    }
    return jsonify(iconos)
