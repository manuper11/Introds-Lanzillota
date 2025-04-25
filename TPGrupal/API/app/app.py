import os
from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_cors import CORS
from .reviews.routes import reviews_bp
from .reservas.routes import reservas_bp
from .users.routes import users_bp
from .habitaciones.routes import habitaciones_bp
from .gestion_precios.routes import gestion_precios_bp
import logging

app = Flask(__name__)
database_url = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://app_user:appMate123@db/flaskdb')

#Creacion de engine
try:
    engine = create_engine(database_url)
    app.config['engine'] = engine
except Exception as e:
    print(f"Error connecting to the database: {e}")

# Configuramos CORS para permitir conexiones solamente desde el frontend
frontend_url = os.getenv('FRONTEND_URL', 'http://127.0.0.1:5001')
CORS(app, resources={r"/*": {"origins": frontend_url}}, supports_credentials=True)

logging.basicConfig(level=logging.INFO)

#Registrar todos los blueprint
app.register_blueprint(reviews_bp, url_prefix='/reviews')
app.register_blueprint(reservas_bp, url_prefix='/reservas')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(habitaciones_bp, url_prefix='/habitaciones')
app.register_blueprint(gestion_precios_bp, url_prefix='/gestion_precios')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)