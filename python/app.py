from flask import Flask, render_template, request, redirect
import psycopg2.extras

app = Flask(__name__)
#Datos para ingresar
#Correo: vito.pimentel@gmail.com
#Contraseña: 1234

#Conectar a la base de datos princial
try:
    connection = psycopg2.connect(
        user = "postgres",
        password = "1234",
        host = "127.0.0.1",
        port = "5432",
        database = "postgres"
    )
    print("Conexión exitosa a PostgreSQL")
except:
    print("Error de conexión a PostgreSQL")

connection.autocommit = True
cursor = connection.cursor()

#Crear base de datos
sql_drop = "DROP DATABASE IF EXISTS \"SIS427VSPV\""
cursor.execute(sql_drop)
sql_db = "CREATE DATABASE \"SIS427VSPV\" WITH OWNER = postgres ENCODING = 'UTF8' LC_COLLATE = 'Spanish_Mexico.1252' LC_CTYPE = 'Spanish_Mexico.1252' TABLESPACE = pg_default CONNECTION LIMIT = -1 IS_TEMPLATE = False;"
cursor.execute(sql_db)
connection.close()

#Conectar a la base de datos creada
try:
    connection = psycopg2.connect(
        user = "postgres",
        password = "1234",
        host = "127.0.0.1",
        port = "5432",
        database = "SIS427VSPV"
    )
    print("Conexión exitosa a PostgreSQL")
except:
    print("Error de conexión a PostgreSQL")

connection.autocommit = True
cursor = connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

#Crear tabla estudiantes
sql_table = "CREATE TABLE IF NOT EXISTS public.\"Estudiante\"(id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ), nombre text COLLATE pg_catalog.\"default\" NOT NULL, apellido text COLLATE pg_catalog.\"default\" NOT NULL, correo text COLLATE pg_catalog.\"default\", password text COLLATE pg_catalog.\"default\", carrera text COLLATE pg_catalog.\"default\" NOT NULL, CONSTRAINT \"Estudiante_pkey\" PRIMARY KEY (id)) TABLESPACE pg_default;" 
cursor.execute(sql_table)

#Agregar un usuario
sql_user = "INSERT INTO public.\"Estudiante\"(nombre, apellido, carrera, correo, password) VALUES('Vito', 'Pimentel', 'Ciencias de la Computacion', 'vito.pimentel@gmail.com', '1234');"
cursor.execute(sql_user)

#Ruta para el log in
@app.route('/')
def index():
    titulo = "Log in"
    return render_template('index.html', title = titulo, wrong_data = False)

#Validacion del log in
@app.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        correo = request.form["correo"]
        password = request.form["password"]
        sql = f"SELECT * FROM public.\"Estudiante\" WHERE correo = '{correo}' AND password = '{password}'"
        cursor.execute(sql)
        validacion = cursor.fetchall()
    if bool(validacion):
        return redirect('/principal')
    titulo = "Log in"
    return render_template('index.html', title = titulo, wrong_data = True)

#Pagina de inicio
@app.route('/principal')
def principal():
    titulo = "Página principal"
    return render_template("principal.html", title = titulo)
        
#Listado de los datos (CRUD)
@app.route('/lista')
def lista():
    titulol = "Lista de Estudiantes"
    sql = "SELECT * FROM public.\"Estudiante\" ORDER BY id ASC"
    cursor.execute(sql)
    estudiantes = cursor.fetchall()
    datos = estudiantes
    return render_template('lista.html', lista = datos, title = titulol)

#Formulario de registro
@app.route("/registro")
def registro():
    return render_template('registro.html')

#Llamada para registrar
@app.route('/guardar', methods = ['POST'])
def guardar():
    if request.method == 'POST':
        nombre = request.form["nombres"]
        apellido = request.form["apellidos"]
        carrera  = request.form["carrera"]
        email = request.form["email"]
        clave = request.form["clave"]
        sql_insert = f"INSERT INTO public.\"Estudiante\"(nombre, apellido, carrera, correo, password) VALUES('{nombre}', '{apellido}', '{carrera}', '{email}', '{clave}');"
        cursor.execute(sql_insert)
    return redirect('/lista')

#Formulario de edicion
@app.route("/editar/<id>", methods = ['GET'])
def editar(id):
    if request.method == 'GET':
        sql = f"SELECT * FROM public.\"Estudiante\" WHERE id = {id}"
        cursor.execute(sql)
        estudiantes = cursor.fetchall()
        datos = estudiantes
    return render_template('editar.html', edatos = datos)

#Llamada para registrar la edición
@app.route("/actualizar/<id>", methods=['POST'])
def actualizar(id):
    nombre = request.form["nombres"]
    apellido = request.form["apellidos"]
    carrera  = request.form["carrera"]
    email = request.form["email"]
    clave = request.form["clave"]
    sql_update = f"UPDATE public.\"Estudiante\" SET nombre='{nombre}', apellido='{apellido}', correo='{email}', password='{clave}', carrera='{carrera}' WHERE id = {id};"
    print(sql_update)
    cursor.execute(sql_update)
    return redirect('/lista')
    
#Llamada para registrar el borrado de un dato
@app.route("/borrar/<id>")
def borrar(id):
    sql_delete = f"DELETE FROM public.\"Estudiante\" WHERE id = {id};"
    print(sql_delete)
    cursor.execute(sql_delete)
    return redirect('/lista')

#Función main
if __name__ == '__main__':
    app.run(debug = True, port = 5000)