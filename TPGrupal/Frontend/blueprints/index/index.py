from blueprints.reviews.reviews import get_random_reviews
from flask import Blueprint, render_template, current_app
import random
import requests

# Crear el blueprint
indexBp = Blueprint('indexBp', __name__)

@indexBp.route('/', methods = ['GET'])
def home():
    reviews = get_random_reviews()
    return render_template('index.html', reviews=reviews)
