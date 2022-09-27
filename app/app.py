from distutils.log import debug
from flask import Flask, render_template


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

# especificamos que si estamos en el archivo main camos a ejecutar la aplicacion 
if __name__ == "__main__":
    app.run(debug=True, port=5000)