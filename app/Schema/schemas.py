from flask_marshmallow import Marshmallow

ma = Marshmallow()

# Esquema Usuario
class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('id', 'usuario', 'password', 'nombre', 'tipo')

