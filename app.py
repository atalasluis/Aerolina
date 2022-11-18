from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os

app = Flask(__name__)
client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.Aerolinea    #Select the database
_vuelos = db.vuelos #Select the collection name

#--------------------- Home -------------------------

@app.route('/')
def home():
    return render_template('index.html')

#----------------- CRUD DE VUELOS -------------------
@app.route('/vuelos')
def vuelos():
    vuelosRecieved=_vuelos.find()
    return render_template('vuelos.html',vuelos=vuelosRecieved)

@app.route('/vuelos/crear')
def vuelos_crear():
    return render_template('vuelos_crear.html')

@app.route('/vuelos/editar')
def vuelos_editar():
    id=request.values.get("idVuelo")
    vuelo =_vuelos.find({"idVuelo":ObjectId(id)})
    print(vuelo)
    return render_template('vuelos_editar.html',vuelos=vuelo)

@app.route("/remove")
def remove ():
    #Deleting a Task with various references
    key=request.values.get("idVuelo")
    print(key)
    _vuelos.delete_one({"idVuelo":ObjectId(key)})
    return redirect("/vuelos")


@app.route("/action", methods=['POST'])
def action ():
    idVuelo=request.values.get("idVuelo")
    fechaSalida=request.values.get("fechaSalida")
    destino=request.values.get("destino")
    capacidad=request.values.get("capacidad")
    aeropuertoOrigen=request.values.get("aeropuertoOrigen")
    aeropuertoDestino=request.values.get("aeropuertoDestino")
    #print(name,' ', desc)
    print(idVuelo)
    _vuelos.insert_one({"idVuelo":idVuelo, "fechaSalida":fechaSalida, "destino":destino, "capacidad":capacidad, "aeropuertoOrigen":aeropuertoOrigen,"aeropuertoDestino":aeropuertoDestino})
    return redirect("/vuelos")

@app.route("/action3", methods=['POST'])
def action3 ():
	#Updating a Task with various references
    fechaSalida=request.values.get("fechaSalida")
    destino=request.values.get("destino")
    capacidad=request.values.get("capacidad")
    aeropuertoOrigen=request.values.get("aeropuertoOrigen")
    aeropuertoDestino=request.values.get("aeropuertoDestino")
    id=request.values.get("idVuelo")
    _vuelos.update_one({"idVuelo":ObjectId(id)}, {'$set':{ "fechaSalida":fechaSalida, "destino":destino, "capacidad":capacidad, "aeropuertoOrigen":aeropuertoOrigen,"aeropuertoDestino":aeropuertoDestino }})
    return redirect("/vuelos")

#----------------- CRUD DE RESERVA ------------------
@app.route('/reserva')
def reserva():
    return render_template('miReserva.html')

#----------------------- PAGOS ----------------------
@app.route('/pagos')

def pagos():
    return render_template('Pagos.html')

#----------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=4000)