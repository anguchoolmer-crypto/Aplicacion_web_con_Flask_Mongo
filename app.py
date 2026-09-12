from flask import Flask
import pymongo

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./static/imagenes"

# Conexión a MongoDB local
miConexion = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
baseDatos = miConexion["ALMACEN"]
productos = baseDatos["PRODUCTOS"]

# Importar el controlador después de definir app y productos
from controllerProducto import *

if __name__ == "__main__":
    app.run(port=3000, debug=True)