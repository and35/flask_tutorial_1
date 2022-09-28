from contextlib import redirect_stderr
from distutils.log import debug
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import  MySQL

app = Flask(__name__, template_folder='templates') # inicializamos una aplicacion 
# creamos una vizualizacion en forma de funcion y la ligamos a la raiz de la app usando el decorador @
@app.route('/')
def index(): 
    temas = ["inmortalidad", "singularidad", "IA", "BCI", "bioprinting"]
    dt= {
        "titulo": "blog h+",
        "bienvenida": "saludos cyborg! ",
        "temas" : temas,
        "n_temas": len(temas)
    }
    return render_template("index.html", data=dt)
    # return "<h1>hola mundo funcion</h1>""

"""URL dinamica"""
@app.route("/contacto/<nombre>")
def contacto(nombre): # "nombre" debe ser el mismo arriba que abajo
    usuarios = {"and35": {"nombre": "andres gutierrez", "profesion": "chief data scientist"}, 
                "tesla3": {"nombre": "nikola tesla", "profesion": "chief enggenering"}}
    data_layout = {
        "titulo": "perfil h+",
        "bienvenida": "informacion del usuario transhumanista "
    }
    # unimos la data del usuario de la URL(se especifica con"nombre") + data del layout contacto 
    data_contacto = data_layout | usuarios[nombre] 
    return render_template("contacto.html", data= data_contacto)


""""URL string"""
def query_string():
    print(request) # nos muestra todo lo que resivio request. es un dic
    print(request.args)
    p1 = request.args.get("param1") # podemos obtener el valor y ahora manipularlo 
    print(p1)
    return "oks!"

"""manejo de errores"""
def pagina_no_encontrada(error):
    return render_template("404.html"), 404 # error indica que se activara ante un error y el 404 indica el tipo de error 
    #return redirect(url_for("index")) # otra opcion es redireccionar al index, es mas comun

"""conectarse a una BBDD """
# 1 datos necesarios para la conexion
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sql123.'
app.config['MYSQL_DB'] = 'sakila'

# 2 creamos la instancia de MySQL en una variable para poder usarla
conexion = MySQL(app)

# 3 creamos una vista 
@app.route("/peliculas")
def listar_peliculas():
    data = {}
    try:
        cursor = conexion.connection.cursor()
        my_query = "SELECT film_id, title, rental_rate FROM film ORDER BY RAND(9) LIMIT 10"
        cursor.execute(my_query)
        pelis = cursor.fetchall()
        data["menasje"] = "exito..."
        data["peliculas"] = pelis
    except Exception as ex:
        data["menasje"] = "error..."
    return jsonify(data) # convertimos el dict a json para mostrar en la pantalla  

# especificamos que si estamos en el archivo main camos a ejecutar la aplicacion 
if __name__ == "__main__":
    app.add_url_rule("/query_string_3", view_func = query_string) #esta es otra opcion en vez de usar el decorador @ 
    app.register_error_handler(404, pagina_no_encontrada)# indicamos el manejador de error
    app.run(debug=True, port=5000)