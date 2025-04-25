from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import bcrypt


users_bp = Blueprint('users', __name__)

@users_bp.route('/<id>', methods=['DELETE'])
def delete_user(id):
    query = text("DELETE FROM Users WHERE id = :id")
    validation_query = text("SELECT * FROM Users WHERE id = :id")
    try:
        engine = current_app.config['engine']
        conn = engine.connect()
        val_result = conn.execute(validation_query, {'id': id})
        if val_result.rowcount == 0:
            conn.close()
            return jsonify({"message": "Usuario no encontrado"}), 404
        conn.execute(query, {'id': id})
        conn.commit()
        conn.close()
        return jsonify({"message": "Usuario eliminado correctamente"}), 200
    except SQLAlchemyError as e:
        error = str(e.__cause__)
        return jsonify({"message": error}) , 500


@users_bp.route('/validar_credenciales', methods=['POST'])
def validar_credenciales():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"success": False, "message": "Email y contraseña son requeridos"}), 400
    
    query = text("SELECT rol, password FROM Users WHERE email = :email")
    try:
        engine = current_app.config['engine']
        conn = engine.connect()
        result = conn.execute(query, {'email': email})
        user = result.fetchone()
        
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404
        
        rol = user[0]
        hashed_password = user[1]

        conn.close()
        
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return jsonify({"success": True, "rol": rol}), 200
        else:
            return jsonify({"success": False, "message": "Credenciales incorrectas"}), 401
    
    except SQLAlchemyError as e:
        error = str(e.__cause__)
        conn.close()
        return jsonify({"success": False, "message": error}) , 500
    

@users_bp.route('/add', methods=['POST'])
def add_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    rol = data.get('rol')
    
    if not email or not password or not rol:
        return jsonify({"message": "Email, contraseña y rol son requeridos"}), 400
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    query = text("INSERT INTO Users (email, password, rol) VALUES (:email, :password, :rol)")
    try:
        engine = current_app.config['engine']
        conn = engine.connect()
        conn.execute(query, {
            'email': email,
            'password': hashed_password.decode('utf-8'),
            'rol': rol
        })
        conn.commit()
        conn.close()
        return jsonify({"message": "Usuario añadido correctamente"}), 201
    
    except SQLAlchemyError as e:
        error = str(e.__cause__)
        return jsonify({"message": error}) , 500