from flask import Blueprint, render_template

nosotrosBp = Blueprint("nosotrosBp", __name__, template_folder='templates')

@nosotrosBp.route('/', methods=["GET"])
def nosotros():
    return render_template('nosotros.html')
