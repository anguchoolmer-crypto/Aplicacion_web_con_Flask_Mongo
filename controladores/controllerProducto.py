from app import app, productos
from flask import Flask, request, render_template, redirect
import pymongo
from werkzeug.utils import secure_filename
import os
from bson.objectid import ObjectId

@app.route("/")
def inicio():
    # Obtener la lista de productos de la colección productos
    listaProductos = productos.find()
    return render_template("listarProductos.html", listaProductos=listaProductos)

# Proceso Agregar Producto
@app.route("/frmAgregarProducto")
def vistaAgregar():
    return render_template("frmAgregarProducto.html")

@app.route("/agregarProducto", methods=["POST"])
def agregarProducto():
    try:
        codigo = int(request.form["txtCodigo"])
        nombre = request.form["txtNombre"]
        precio = int(request.form["txtPrecio"]) 
        categoria = request.form["cbCategoria"]
        
        archivo = request.files["fileFoto"]
        nombreArchivo = secure_filename(archivo.filename)
        listaNombreArchivo = nombreArchivo.rsplit(".", 1)
        extension = listaNombreArchivo[1].lower()

        producto = {
            "codigo": codigo,
            "nombre": nombre,
            "precio": precio,
            "categoria": categoria
        }

        if consultarProductoPorCodigo(codigo):
            mensaje = "Ya existe producto con ese código"
            return render_template("frmAgregarProducto.html", producto=producto, mensaje=mensaje)
        else:
            resultado = productos.insert_one(producto)
            if resultado.acknowledged:
                idProducto = resultado.inserted_id
                nuevoNombre = str(idProducto) + "." + str(extension)
                archivo.save(os.path.join(app.config["UPLOAD_FOLDER"], nuevoNombre))
                return redirect("/")
    except pymongo.errors.PyMongoError as error:
        return render_template("frmAgregarProducto.html", producto=producto, mensaje=str(error))

def consultarProductoPorCodigo(codigo):
    try:
        consulta = {"codigo": codigo}
        producto = productos.find_one(consulta)
        return producto is not None
    except pymongo.errors.PyMongoError as error:
        print(error)
        return False

# Proceso Consultar por ID para Editar
@app.route("/consultar/<string:idProducto>", methods=["GET"])
def consultarPorId(idProducto):
    try:
        obj_id = ObjectId(idProducto)
        consulta = {"_id": obj_id}
        producto = productos.find_one(consulta)
        return render_template("frmEditarProducto.html", producto=producto)
    except pymongo.errors.PyMongoError as error:
        listaProductos = productos.find()
        return render_template("listarProductos.html", mensaje=str(error), listaProductos=listaProductos)

# Proceso Actualizar
@app.route("/actualizar", methods=["POST"])
def actualizarProducto():
    try:
        codigo = int(request.form["txtCodigo"])
        nombre = request.form["txtNombre"]
        precio = int(request.form["txtPrecio"])
        categoria = request.form["cbCategoria"]
        idProducto = ObjectId(request.form["idProducto"])

        criterio = {"_id": idProducto}
        datosActualizar = {
            "codigo": codigo,
            "nombre": nombre,
            "precio": precio,
            "categoria": categoria
        }
        consulta = {"$set": datosActualizar}
        resultado = productos.update_one(criterio, consulta)

        if resultado.acknowledged:
            archivo = request.files["fileFoto"]
            if archivo and archivo.filename != "":
                nombreArchivo = secure_filename(archivo.filename)
                listaNombreArchivo = nombreArchivo.rsplit(".", 1)
                extension = listaNombreArchivo[1].lower()
                nombreArchivoActualizar = str(idProducto) + "." + str(extension)
                archivo.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreArchivoActualizar))
        return redirect("/")
    except pymongo.errors.PyMongoError as error:
        return redirect("/")

# Proceso Eliminar
@app.route("/eliminar/<string:idProducto>", methods=["GET"])
def eliminarProducto(idProducto):
    try:
        obj_id = ObjectId(idProducto)
        consulta = {"_id": obj_id}
        productos.delete_one(consulta)
        return redirect("/")
    except pymongo.errors.PyMongoError as error:
        listaProductos = productos.find()
        return render_template("listarProductos.html", mensaje=str(error), listaProductos=listaProductos)