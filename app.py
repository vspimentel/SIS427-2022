from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    persona = {"nombre":"Juan", "apellido":"Perez", "correo":"juanperez@gmail.com"}

    titulo = "Pagina principal"
    return render_template('index.html', title = titulo, per = persona)

if __name__ == '__main__':
    app.run(debug = True, port = 5000)