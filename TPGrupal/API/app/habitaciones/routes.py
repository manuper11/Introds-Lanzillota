# API/app/habitaciones/routes.py
from flask import Blueprint, jsonify, request, current_app
from flask import jsonify
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

habitaciones_bp = Blueprint('habitaciones',__name__)
@habitaciones_bp.route('/', methods=['GET'])
def get_habitaciones():
    query = text("SELECT id, nombre, descripcion, precio_noche, personas_max, url_imagen FROM Habitaciones")
    try:
        engine = current_app.config['engine']
        with engine.connect() as conn: 
            result = conn.execute(query)
    except SQLAlchemyError as err:
        error_message = str(err.__cause__) if err.__cause__ else str(err)
        return jsonify({'message': "Se ha producido un error: " + error_message}), 500
    habitaciones = []

    for h in result:
        entrada = {}
        entrada['id']= h.id
        entrada['nombre']=h.nombre
        entrada['descripcion']=h.descripcion
        entrada['precio_noche']=h.precio_noche
        entrada['personas_max']=h.personas_max
        entrada['url_imagen']=h.url_imagen 
        habitaciones.append(entrada)

    return jsonify(habitaciones),200


