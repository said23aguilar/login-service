from database import db
# En esta parte se crearan los modelos necesarios para la creacion de las tablas de las bases de datos
#--------------------------------- Modelo Usuario ----------------------------------------- #
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key = True)
    usuario = db.Column(db.String(70), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable = False)
    nombre = db.Column(db.String(50), nullable = False, unique=True)
    tipo = db.Column(db.Integer, nullable = False)

    def __init__(self, usuario, password, nombre, tipo):
        self.usuario = usuario
        self.password = password
        self.nombre = nombre
        self.tipo = tipo



