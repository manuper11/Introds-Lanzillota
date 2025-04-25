from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# ---Crear Blueprint para reviews ---
reviews_bp = Blueprint('reviews', __name__)

# ---Crear las rutas con el blueprint---
# --- Crear review ---
@reviews_bp.route('/', methods=['POST'])
def create_review():
    new_review = request.get_json()
    
    # --- Me aseguro que la request venga con nombre_autor y texto ----
    if not new_review or 'nombre_autor' not in new_review or 'texto' not in new_review or 'reserva_id' not in new_review:
        return jsonify({'message': "Datos incompletos"}), 400
    if new_review['nombre_autor'].strip() == '' or new_review['texto'].strip() == '':
        return jsonify({'message': "Los campos no deben contener solo espacios en blanco."}), 400
    if len(new_review['texto'].split()) < 5:
        return jsonify({'message': "El campo de texto debe contener al menos 5 palabras."}), 400
    
    nombre_autor = new_review['nombre_autor']
    texto = new_review['texto']
    reserva_id = new_review['reserva_id']

    # Validaciones de longitud
    if len(nombre_autor) > 80:
        return jsonify({'message': "El nombre del autor no debe exceder los 80 caracteres."}), 400
    if len(texto) > 150:
        return jsonify({'message': "El texto de la review no debe exceder los 150 caracteres."}), 400
    
    # Verificar si ya existe una review con el mismo reserva_id
    query_check = text("SELECT COUNT(*) FROM Reviews WHERE reserva_id = :reserva_id")
    query_insert = text("INSERT INTO Reviews (nombre_autor, texto, reserva_id) VALUES (:nombre_autor, :texto, :reserva_id)")

    try:
        engine = current_app.config['engine']
        with engine.connect() as conn: 
            result = conn.execute(query_check, {'reserva_id': reserva_id}).scalar()
            if result > 0:
                return jsonify({'message': "Ya existe una review para esta reserva."}), 400
            
            conn.execute(query_insert, {'nombre_autor': nombre_autor, 'texto': texto, 'reserva_id': reserva_id})
            conn.commit()
    except SQLAlchemyError as err:
        error_message = str(err.__cause__) if err.__cause__ else str(err)
        return jsonify({'message': "Se ha producido un error: " + error_message}), 500
    
    return jsonify({'message': "Se ha agregado correctamente"}), 201

# ---Actualizar el estado de visibilidad ---
@reviews_bp.route('/<int:id>/visibility', methods=['PUT'] ) 
def update_visibility(id):
    new_status= request.get_json().get('visible')
    # --- Me aseguro que la request venga con un status----
    if new_status is None:
        return jsonify({'message': "Datos incompletos"}), 400
    query = text("UPDATE Reviews SET visible = :visible WHERE id= :id")
    try:
        engine = current_app.config['engine']
        with engine.connect() as conn: 
            result = conn.execute(query, {'visible': new_status, 'id': id})
            conn.commit()
            # --- Verifica si existe una review para el id ----
            if  result.rowcount == 0:
                return jsonify({'message': 'Review no encontrada para el id especificado'}), 404
    except SQLAlchemyError as err:
        error_message = str(err.__cause__) if err.__cause__ else str(err)
        return jsonify({'message': "Se ha producido un error: " + error_message}), 500
    
    return jsonify({'message': "Se ha modificado la visibilidad correctamente"}), 200

# ---Actualizar la columna estado ---
@reviews_bp.route('/<int:id>/state', methods=['PUT'] ) 
def update_state(id):
    new_status= request.get_json().get('estado')
    # --- Me aseguro que la request venga con un status----
    if new_status is None:
        return jsonify({'message': "Datos incompletos"}), 400
    query = text("UPDATE Reviews SET estado = :estado WHERE id= :id")
    try:
        engine = current_app.config['engine']
        with engine.connect() as conn: 
            result = conn.execute(query, {'estado': new_status, 'id': id})
            conn.commit()
            # --- Verifica si existe una review para el id ----
            if  result.rowcount == 0:
                return jsonify({'message': 'Review no encontrada para el id especificado'}), 404
    except SQLAlchemyError as err:
        error_message = str(err.__cause__) if err.__cause__ else str(err)
        return jsonify({'message': "Se ha producido un error: " + error_message}), 500
    
    return jsonify({'message': "Se ha modificado el estado correctamente"}), 200

# --- Obtener todas las reviews (para el administrador) ---
@reviews_bp.route('/', methods=['GET'])
def get_all_reviews():
    query = text("SELECT * FROM Reviews")
    try:
        engine = current_app.config['engine']
        with engine.connect() as conn: 
            result = conn.execute(query)
    except SQLAlchemyError as err:
        error_message = str(err.__cause__) if err.__cause__ else str(err)
        return jsonify({'message': "Se ha producido un error: " + error_message}), 500
    
    reviews = []
    for row in result:
        entity = {}
        entity['id'] = row.id
        entity['nombre_autor'] = row.nombre_autor
        entity['texto'] = row.texto
        entity['visible'] = row.visible
        entity['estado']= row.estado
        entity['reserva_id']= row.reserva_id
        reviews.append(entity)

    return jsonify(reviews), 200

# --- Obtener todas las reviews con visibilidad confirmada (para el main) ---
@reviews_bp.route('/visible', methods=['GET'])
def get_visible_reviews():
    query = text("SELECT * FROM Reviews WHERE visible = true")
    try:
        engine = current_app.config['engine']
        with engine.connect() as conn:
            result = conn.execute(query)
    except SQLAlchemyError as err:
        error_message = str(err.__cause__) if err.__cause__ else str(err)
        return jsonify({'message': "Se ha producido un error: " + error_message}), 500
    
    reviews = []
    for row in result:
        entity = {}
        entity['id'] = row.id
        entity['nombre_autor'] = row.nombre_autor
        entity['texto'] = row.texto
        entity['visible'] = row.visible
        entity['estado']= row.estado
        entity['reserva_id']= row.reserva_id
        reviews.append(entity)

    return jsonify(reviews), 200    


@reviews_bp.route('/<int:id>/delete', methods=['DELETE'])
def delete_review(id):
    delete_query = text("DELETE FROM Reviews WHERE id = :id")
    validation_query = text("SELECT * FROM Reviews WHERE id = :id")
    try:
        engine = current_app.config['engine']
        with engine.connect() as conn:
            val_result = conn.execute(validation_query, {'id': id})
            if val_result.rowcount == 0:
                return jsonify({"message": "Review no encontrada"}), 404
            conn.execute(delete_query, {'id': id})
            conn.commit()
    except SQLAlchemyError as err:
        error_message = str(err.__cause__) if err.__cause__ else str(err)
        return jsonify({'message': "Se ha producido un error: " + error_message}), 500    
    return jsonify({"message": "Review eliminada correctamente"}), 200
