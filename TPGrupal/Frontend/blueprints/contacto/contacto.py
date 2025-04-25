from flask import Blueprint, jsonify, request, render_template, url_for, redirect, flash
import smtplib
from email.mime.text import MIMEText

contactoBp = Blueprint("contactoBp", __name__, template_folder='templates')

@contactoBp.route('/', methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        nombre = request.form.get("name")
        email = request.form.get("email")
        asunto = request.form.get("subject")
        mensaje_contenido = request.form.get("message")

        mensaje_completo = (f"NOMBRE: {nombre}\n"
                            f"MAIL: {email}\n"
                            f"MENSAJE:\n{mensaje_contenido}")

        mensaje = MIMEText(mensaje_completo)

        mensaje["Subject"] = asunto
        mensaje["From"] = "hotel.glaciar.argentina@gmail.com"
        mensaje["To"] = "hotel.glaciar.argentina@gmail.com"

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login("hotel.glaciar.argentina@gmail.com", "oqvu xdib bmnp ymzy")
            smtp_server.sendmail("hotel.glaciar.argentina@gmail.com", "hotel.glaciar.argentina@gmail.com", mensaje.as_string())
            
        flash('Su mensaje fue enviado!! Responderemos lo mas rapido que podamos.', 'success')

        return redirect(url_for("contactoBp.contacto"))
    return render_template('contacto.html')