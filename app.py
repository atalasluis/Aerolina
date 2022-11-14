from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os


app = Flask(__name__)
client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.Aerolinea    #Select the database
_vuelos = db.vuelos #Select the collection name

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/vuelos')
def vuelos():
    vuelosRecieved=_vuelos.find()
    return render_template('vuelos.html',vuelos=vuelosRecieved)

@app.route('/vuelos/crear')
def vuelos_crear():
    return render_template('vuelos_crear.html')

@app.route("/action", methods=['POST'])
def action ():
    idVuelo=request.values.get("idVuelo")
    fechaSalida=request.values.get("fechaSalida")
    destino=request.values.get("destino")
    capacidad=request.values.get("capacidad")
    aeropuertoOrigen=request.values.get("aeropuertoOrigen")
    aeropuertoDestino=request.values.get("aeropuertoDestino")
    #print(name,' ', desc)
    _vuelos.insert_one({"idVuelo":idVuelo, "fechaSalida":fechaSalida, "destino":destino, "capacidad":capacidad, "aeropuertoOrigen":aeropuertoOrigen,"aeropuertoDestino":aeropuertoDestino})
    return redirect("/vuelos")
if __name__ == '__main__':
    app.run(debug=True, port=4000)