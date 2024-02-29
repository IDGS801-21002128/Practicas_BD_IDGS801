from wtforms import validators,Form,StringField,IntegerField,EmailField,FloatField

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