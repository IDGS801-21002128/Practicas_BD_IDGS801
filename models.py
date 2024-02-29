from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Empleado(db.Model):
    _tablename_ = "empleados"
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(50))
    direccion=db.Column(db.String(50))
    telefono=db.Column(db.Integer)
    email=db.Column(db.String(50))
    sueldo=db.Column(db.Float)
    created_date=db.Column(db.DateTime,default=datetime.datetime.now)
