from flask import *
from forms import UserForm, PedidoForm
from flask_wtf.csrf import CSRFProtect
from config import DevelomentConfig
from models import db
from models import Empleado, Pedido, PedidoTotal
from datetime import datetime, date
from sqlalchemy import func
from sqlalchemy import extract

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
    pedidoBD = PedidoTotal.query.all()
    formulario = PedidoForm(request.form)
    total_subtotales = sum(pedido.total_pedidos for pedido in pedidoBD)
    formulario.id.validators = []
    precio_total = 0 
    total=0

    if request.method == "GET":
        # Cambiado a request.args.get para solicitudes GET
        dia_semana = int(request.args.get('fecha_dia')) if request.args.get('fecha_dia') else None
        mes = int(request.args.get('fecha_mes')) if request.args.get('fecha_mes') else None
        
        # Inicializamos vFecha con todos los pedidos si no se aplican filtros
        vFecha = pedidoBD
        print(dia_semana)
        print("FORM")
        # Aplicar filtros según los parámetros proporcionados
        if dia_semana is not None :
            print(dia_semana)
            print(mes)
            if dia_semana == 7:  # Si es domingo
                dia_semana = 1  # Domingo es 1 en MySQL
            elif dia_semana >0 :
                dia_semana = dia_semana + 1  # Ajuste para otros días

            if  dia_semana > 0 and mes == 1:
                vFecha = PedidoTotal.query.filter(func.dayofweek(PedidoTotal.fecha_pedido) == (dia_semana)).all()
                print(vFecha)
        if mes is not None:
            if mes > 1 and dia_semana ==0:
                vFecha = PedidoTotal.query.filter(extract('month', PedidoTotal.fecha_pedido) == mes).all()
        
        total_subtotales = sum(pedido.total_pedidos for pedido in vFecha)
        
        return render_template('pedidos.html', total_subtotales=total_subtotales, pedidosb=vFecha, form=formulario)


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
                        fechaCompra=formulario.fecha.data,
                        tamañoPizza=formulario.tamañoPizza.data,
                        ingredientes='',
                        numPizza=formulario.numPizza.data,
                        precioTotal=precio_total)
        print(pedido)
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
        total = sum(pedido.precioTotal for pedido in pedidos)


    return render_template('pedidos.html',total_subtotales=total_subtotales, total=total,pedidosb=pedidoBD,form=formulario, pedidos=pedidos, precio_total= precio_total)

@app.route('/terminar', methods=['POST'])
def terminar_pedido():
    print(pedidos)
    nombre_cliente = pedidos[0].nombre if pedidos else None
  
    if nombre_cliente is not None:
        total_pedidos = sum(pedido.precioTotal for pedido in pedidos)
        fecha_pedido = pedidos[0].fechaCompra 
        print(fecha_pedido)
        pedido_terminado = PedidoTotal(nombre_cliente=nombre_cliente, total_pedidos=total_pedidos, fecha_pedido=fecha_pedido)
        db.session.add(pedido_terminado)
        db.session.commit()
        print("SE INSERTO")
    return redirect(url_for('pagina_confirmacion'))

@app.route('/confirmacion')
def pagina_confirmacion():
    mensaje_confirmacion = "¡Tu pedido ha sido confirmado exitosamente!"

    limpiar_lista_pedidos()

    return render_template('confirmacion.html', mensaje_confirmacion=mensaje_confirmacion)
def limpiar_lista_pedidos():
    global pedidos
    pedidos = [] 

@app.route('/eliminarPedido/<int:pedido_id>', methods=['GET', 'POST'])
def eliminarPedido(pedido_id):
    pedidos.pop(pedido_id)
    return redirect(url_for('realizar_pedido'))


@app.route('/modificar_pedido/<int:pedido_id>', methods=['GET', 'POST'])
def modificar_pedido(pedido_id):
    print(pedidos)
    calcular_precio_total = 0
    pedido = pedidos[pedido_id]  
    print(pedido)
    if request.method == 'POST':
        pedido.tamañoPizza = request.form['tamañoPizza']
        pedido.ingredientes = request.form['ingredientes']
        pedido.numPizza = request.form['numPizza']
        pedido.precioTotal = calcular_precio_total(pedido.tamañoPizza, pedido.numPizza) 
        return redirect(url_for('pedidos'))

    return render_template('modificar_pedido.html', pedido=pedido)


@app.route('/buscar_pedido', methods=['POST'])
def buscar_pedido():
    dia_semana = int(request.form.get('fecha_dia')) if request.form.get('fecha_dia') else None  # Obtener el día de la semana seleccionado del formulario
    mes = int(request.form.get('fecha_mes')) if request.form.get('fecha_mes') else None  # Obtener el mes seleccionado del formulario y convertirlo a entero
    buscar_por = request.form.get('buscar_por')
    print(dia_semana)
    vFecha = PedidoTotal.query.all()
    
    if dia_semana is not None and mes is not None:
        if dia_semana == 0 and mes > 0:
            vFecha = PedidoTotal.query.filter(extract('month', PedidoTotal.fecha_pedido) == mes).all()
        elif mes == 0 and dia_semana > 0:
            vFecha = PedidoTotal.query.filter(extract('weekday', PedidoTotal.fecha_pedido) == dia_semana).all()
            print(vFecha)
    total_subtotales = sum(pedido.total_pedidos for pedido in vFecha) if vFecha else 0
    formulario = PedidoForm(request.form)
    total_subtotales_existente = sum(pedido.total_pedidos for pedido in vFecha)
    formulario.id.validators = []
    precio_total_existente = 0 

    return render_template('pedidos.html', 
                            total_subtotales=total_subtotales,
                            total_subtotales_existente=total_subtotales_existente,
                            pedidosb=vFecha,
                            form=formulario, 
                            precio_total_existente=precio_total_existente)

if __name__=="__main__":
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
    app.run()