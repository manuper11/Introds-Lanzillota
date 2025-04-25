from flask import Flask, url_for, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def Home():
    nombre = "Emanuel"
    apellido = "Perez Martinez"
    return render_template("home.html", nombre=nombre, apellido=apellido)
@app.route("/datos_personales", methods=['GET', 'POST'])
def Formulario():
    if request.method == "POST":
        nombre_alumno = request.form.get("fnombre")
        apellido_alumno = request.form.get("fapellido")
        celular = request.form.get("fcelular")
        direc = request.form.get("fdirec")
        dni = request.form.get("fdni")
        lista = [nombre_alumno,apellido_alumno,celular,direc,dni]
        return render_template("aceptado.html", lista=lista)
    else:
        return render_template("formulario.html")

if __name__ == "__main__":
    app.run("127.0.0.1", port="8080", debug=True)