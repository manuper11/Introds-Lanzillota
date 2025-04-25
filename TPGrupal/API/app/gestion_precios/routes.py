from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# ---Crear Blueprint para gestion de precios ---
gestion_precios_bp = Blueprint('gestion_precios', __name__)

# Función que maneja una request PATCH para actualizar el precio 
# de una habitación en la base de datos. 
# Ejecuta la query y devuelve respuestas JSON según modificó correctamente
# o si encontró un error.

@gestion_precios_bp.route('/gestion_precios', methods=['PATCH'])
def actualizar_precios_habitaciones():
    datos = request.get_json()
    nuevo_precio = datos.get('precio_noche')
    id_habitacion = datos.get('id')    
    
    query = text("UPDATE Habitaciones SET precio_noche = :precio_noche WHERE id = :id")        
    try:          
        connection = current_app.config['engine'].connect()
        result = connection.execute(query, {'precio_noche': nuevo_precio, 'id': id_habitacion})
        if result.rowcount == 0:
            connection.close()
            return jsonify({'message': 'Habitación no encontrada'}), 404 
        else:
            connection.commit()
            connection.close()
            return jsonify({'message': 'Precio actualizado correctamente'}), 200
    except SQLAlchemyError as e:
        error = str(e.__cause__)
        return jsonify({'message': error}), 500