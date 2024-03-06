from wtforms import validators,Form,StringField,IntegerField,EmailField,FloatField,DateField,RadioField, BooleanField
from wtforms.validators import DataRequired, Length

class UserForm(Form):
    id = IntegerField('id',[validators.number_range(min=1, max=20, message='Valor no válido')])
    nombre = StringField("nombre",[
        validators.DataRequired(message='El campo es requerido.'),
        validators.length(min=4,max=10,message='El minimo es 4 y el máximo es 10'),
    ])
    direccion = StringField("direccion",[
        validators.DataRequired(message='El campo es requerido.'),
        validators.length(min=4,max=10,message='El minimo es 4 y el máximo es 10')
    ])
    telefono = IntegerField("telefono",[
        validators.DataRequired(message='El campo es requerido.'),
    ])
    email = EmailField("email",[
        validators.Email(message='Ingrese un email válido!')
    ])
    sueldo = FloatField("sueldo",[
        validators.DataRequired(message='El campo es requerido.'),
    ])

class PedidoForm(Form):
    id = IntegerField('id', [validators.number_range(min=1, max=20, message='Valor no válido')])
    nombre = StringField('Nombre Completo', validators=[DataRequired(), Length(min=2, max=100)])
    direccion = StringField('Dirección', validators=[DataRequired(), Length(min=2, max=200)])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(min=7, max=15)])
    tamañoPizza = RadioField('Tamaño de la Pizza', choices=[('pequena', 'Pequeña $40'), ('mediana', 'Mediana $80'), ('grande', 'Grande $120')], validators=[DataRequired()])
    jamon = BooleanField('Jamón')
    piña = BooleanField('Piña')
    champiñon = BooleanField('Champiñón')
    numPizza = IntegerField('Número de Pizzas', validators=[DataRequired()])