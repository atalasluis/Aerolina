from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os

app = Flask(__name__)
client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.Aerolinea    #Select the database
_vuelos = db.vuelos #Select the collection name
_reserva = db.reserva

#--------------------- Home -------------------------

@app.route('/')
def home():
    return render_template('index.html')

#----------------- CRUD DE VUELOS -------------------
@app.route('/vuelos')
def vuelos():
    vuelosRecieved=_vuelos.find()
    return render_template('vuelos.html',vuelos=vuelosRecieved)

#Method create
@app.route('/vuelos/crear')
def vuelos_crear():
    return render_template('vuelos_crear.html')

@app.route("/action", methods=['POST'])
def action ():
    idVuelo=request.values.get("idVuelo")
    fechaSalida=request.values.get("fechaSalida")
    destino=request.values.get("destino")
    capacidad=request.values.get("capacidad")
    disponibilidad=request.values.get("disponibilidad")
    costo=request.values.get("costo")
    aeropuertoOrigen=request.values.get("aeropuertoOrigen")
    aeropuertoDestino=request.values.get("aeropuertoDestino")
    #print(name,' ', desc)
    print(idVuelo)
    _vuelos.insert_one({"idVuelo":idVuelo, "fechaSalida":fechaSalida, "destino":destino, "capacidad":capacidad, "disponibilidad":disponibilidad, "costo":costo, "aeropuertoOrigen":aeropuertoOrigen,"aeropuertoDestino":aeropuertoDestino})
    return redirect("/vuelos")

#Method update
@app.route("/edit/<string:vuelo_id>", methods=['POST'])
def action3 (vuelo_id):
	#Updating a Task with various references
    fechaSalida=request.values.get("fechaSalida")
    destino=request.values.get("destino")
    capacidad=request.values.get("capacidad")
    disponibilidad=request.values.get("disponibilidad")
    costo=request.values.get("costo")
    aeropuertoOrigen=request.values.get("aeropuertoOrigen")
    aeropuertoDestino=request.values.get("aeropuertoDestino")
    _vuelos.update_one({"idVuelo":vuelo_id}, {'$set':{ "fechaSalida":fechaSalida, "destino":destino, "capacidad":capacidad, "disponibilidad":disponibilidad, "costo":costo, "aeropuertoOrigen":aeropuertoOrigen,"aeropuertoDestino":aeropuertoDestino }})
    return redirect("/vuelos")

#Method delete
@app.route("/remove/<string:vuelo_id>")
def remove (vuelo_id):
    _vuelos.delete_one({'idVuelo' : vuelo_id})
    return redirect("/vuelos")

#----------------- CRUD DE RESERVA ------------------
@app.route('/reserva')
def reserva():
    vuelosRecieved=_vuelos.find()
    return render_template('miReserva.html',vuelos=vuelosRecieved)

#create reserva
@app.route("/action/crear_reserva", methods=['POST'])
def create_reserva ():
    ciPasajero=request.values.get("CI_pasajero")
    nombre_pasajero=request.values.get("Nombre_Pasajero")
    idVuelo=request.values.get("ID_Vuelo")
    asiento=request.values.get("Asiento")
    print(ciPasajero)
    _reserva.insert_one({"ciPasajero":ciPasajero, "nombre_pasajero":nombre_pasajero, "idVuelo":idVuelo, "asiento":asiento})
    return redirect("/reserva")

#----------------------- PAGOS ----------------------
@app.route('/pagos')
def pagos():
    return render_template('Pagos.html')

#buscar reserva
@app.route("/pago_tarjeta", methods=['GET'])
def actionPago ():
    ciPasajero=request.values.get("CI_pasajero")
    print(ciPasajero)
    reservaRecieved=_reserva.find({"ciPasajero":ciPasajero})
    print(reservaRecieved)
    idVuelo=_reserva.find({"ciPasajero":ciPasajero},{"idVuelo": "true", "_id": "false"})
    print(idVuelo)
    vueloRecived=_vuelos.find({"idVuelo":idVuelo})
    #print(vueloRecived)
    return render_template('Pagos_Tarjeta.html',reserva=reservaRecieved,vuelo=vueloRecived)
#posible solucion $lookup
#----------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=4000)