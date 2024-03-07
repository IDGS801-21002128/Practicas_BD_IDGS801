from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime


db = SQLAlchemy()

class Empleado(db.Model):
    _tablename_ = "empleados"
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(50))
    direccion=db.Column(db.String(50))
    telefono=db.Column(db.Integer)
    email=db.Column(db.String(50))
    sueldo=db.Column(db.Float)
    created_date = db.Column(db.DateTime, default=datetime.now)



class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(15))
    fechaCompra = db.Column(db.Date)
    tamañoPizza = db.Column(db.String(50))
    ingredientes = db.Column(db.String(150))  # Cambiado a 150 para manejar múltiples ingredientes
    numPizza = db.Column(db.Integer)
    precioTotal = db.Column(db.Float)  # Se agrega un campo para el precio total
    created_date = db.Column(db.DateTime, default=datetime.now)
