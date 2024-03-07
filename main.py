from flask import *
from forms import UserForm, PedidoForm
from flask_wtf.csrf import CSRFProtect
from config import DevelomentConfig
from models import db
from models import Empleado, Pedido
from datetime import datetime

# Luego, en tu código, puedes usar datetime.now() para obtener la fecha y hora actuales
fechaCompra = datetime.now()
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
        
    return render_template("index.html", form=formulario)

##@app.errorhandler(404)
#def page_noit_found():
#    return render_template("404.html"),404

#@app.before_request
#def before_request():
#    g.nombre="Mario"
#    print("Before 1")

#@app.after_request
#def after_request(response):
#        print("after 3")
#        return response
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


############################ Pizzeria################################

pedidos =[]
precios_pizza = {'pequena': 40, 'mediana': 80, 'grande': 120}
precios_ingredientes = {'jamon': 10, 'piña': 10, 'champiñon': 10}
@app.route('/pedido', methods=['GET', 'POST'])
def realizar_pedido():
   
    formulario = PedidoForm(request.form)
    total_subtotales = sum(pedido.precioTotal for pedido in pedidos)
    formulario.id.validators = []
    precio_total = 0 
    if request.method == 'POST' and formulario.validate():
       
        
        precio_pizza = precios_pizza[formulario.tamañoPizza.data]
        precio_total += precio_pizza
        
        if formulario.jamon.data:
            precio_total += precios_ingredientes['jamon']
        if formulario.piña.data:
            precio_total += precios_ingredientes['piña']
        if formulario.champiñon.data:
            precio_total += precios_ingredientes['champiñon']
        
        precio_total *= formulario.numPizza.data

        pedido = Pedido(nombre=formulario.nombre.data, 
                        direccion=formulario.direccion.data,
                        telefono=formulario.telefono.data,
                        fechaCompra=datetime.now(),
                        tamañoPizza=formulario.tamañoPizza.data,
                        ingredientes='',
                        numPizza=formulario.numPizza.data,
                        precioTotal=precio_total)
       
        ingredientes_seleccionados = []
        if formulario.jamon.data:
            ingredientes_seleccionados.append('Jamón')
        if formulario.piña.data:
            ingredientes_seleccionados.append('Piña')
        if formulario.champiñon.data:
            ingredientes_seleccionados.append('Champiñón')

        pedido.ingredientes = ', '.join(ingredientes_seleccionados)

        pedidos.append(pedido)
        print(pedidos)

        formulario.populate_obj(type('obj', (object,), {}))

        return redirect(url_for('realizar_pedido'))


    return render_template('pedidos.html',total_subtotales=total_subtotales, form=formulario, pedidos=pedidos, precio_total= precio_total)

@app.route('/eliminarPedido/<int:pedido_id>', methods=['GET', 'POST'])
def eliminarPedido(pedido_id):
    pedidos.pop(pedido_id)
    return redirect(url_for('realizar_pedido'))


@app.route('/modificar_pedido/<int:pedido_id>', methods=['GET', 'POST'])
def modificar_pedido(pedido_id):
    print(pedidos)

    # Aquí deberías obtener el pedido con el ID proporcionado, por ejemplo, desde una base de datos
    pedido = pedidos[pedido_id]  # Debes implementar esta función
    print(pedido)
    if request.method == 'POST':
        # Si se envió un formulario POST, actualiza los detalles del pedido con los datos del formulario
        pedido.tamañoPizza = request.form['tamañoPizza']
        pedido.ingredientes = request.form['ingredientes']
        pedido.numPizza = request.form['numPizza']
        pedido.precioTotal = calcular_precio_total(pedido.tamañoPizza, pedido.numPizza)  # Debes implementar esta función
        # Luego, guarda los cambios en la base de datos, si es necesario

        # Redirige a la página de pedidos después de la modificación
        return redirect(url_for('pedidos'))

    # Si se solicita la página con un método GET, muestra el formulario de modificación con los detalles del pedido
    return render_template('modificar_pedido.html', pedido=pedido)


# Ruta para la página de confirmación
@app.route('/confirmacion')
def confirmacion():
    # Aquí manejas la lógica para mostrar la confirmación del pedido
    return render_template('confirmacion.html')



if __name__=="__main__":
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
    app.run()