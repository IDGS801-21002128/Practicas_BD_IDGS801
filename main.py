from flask import *
from forms import UserForm
from flask_wtf.csrf import CSRFProtect
from config import DevelomentConfig
from models import db
from models import Empleado

app=Flask(__name__)
app.config.from_object(DevelomentConfig)
csrf=CSRFProtect()

@app.route("/empleado", methods=[ "GET", "POST"])
def empleadoGet():
    empleado = Empleado.query.all()
    return render_template("ABC_Completo.html", empleados=empleado)

@app.route("/",methods=['GET','POST'])
def index():
    formulario = UserForm(request.form)
    formulario.id.validators = []
    if request.method == 'POST' and formulario.validate() :
        empleado = Empleado(nombre = formulario.nombre.data, 
                         direccion = formulario.direccion.data,
                         telefono = formulario.telefono.data,
                         email = formulario.email.data,
                         sueldo = formulario.sueldo.data)
        db.session.add(empleado)
        db.session.commit()
        print("Finalizó")
    return render_template("index.html", form=formulario)

@app.errorhandler(404)
def page_noit_found():
    return render_template("404.html"),404

@app.before_request
def before_request():
    g.nombre="Mario"
    print("Before 1")

@app.after_request
def after_request(response):
        print("after 3")
        return response
@app.route("/alumno",methods=['GET','POST'])
def alumno():
    print("alumno: {}".format(g.nombre))
    alumno_clase = UserForm(request.form)
    nombre,apaterno='',""
    amaterno=''
    email=""
    numeroCelular=''
    if request.method == "POST" and alumno_clase.validate():
       nombre=alumno_clase.nombre.data
       ##email= alumno_clase.email
       apaterno=alumno_clase.apaterno.data
       amaterno=alumno_clase.amaterno.data
       numeroCelular=alumno_clase.numeroCelular
       
       mensaje="BIENVENIDO  {}".format(nombre)
       flash(mensaje )

    return render_template("alumno.html",form=alumno_clase,nombre=nombre,apaterno=apaterno,amaterno=amaterno,numeroCelular=numeroCelular,email=email)



if __name__=="__main__":
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
    app.run()