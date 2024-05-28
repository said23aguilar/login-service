#Importamos las librerias necesarias
import os
from flask import Flask
from database import db
from sqlalchemy_utils import create_database, database_exists
from Routes.routes import blue_print
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import datetime
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt


app = Flask(__name__)

jwt = JWTManager(app)



load_dotenv()

HOST = os.getenv("DB_HOST")
NAME = os.getenv("DB_NAME")
USUARIO = os.getenv("DB_USUARIO")
PASSWORD = os.getenv("DB_PASSWORD")
PORT_HOST = os.getenv("HOST_PORT")

JWT_SECRET_API = os.getenv("JWT_SECRET")
JWT_LOCATION_API = os.getenv("JWT_LOCATION")

DB_URL = f'mysql+pymysql://{USUARIO}:{PASSWORD}@{HOST}:46513/{NAME}'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = JWT_SECRET_API
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=12)
app.config['CORS_ORIGINS'] = ['/auth/registrar', '/auth/login', '/auth/perfil']
bcrypt = Bcrypt(app)
#CORS(app, )
# Iniciamos SQLAlchemy
db.init_app(app)

#Instanciamos las Rutas
app.register_blueprint(blue_print)

#Creamos o verificamos que este la bd
with app.app_context():
    if not database_exists(DB_URL):
        create_database(DB_URL)
    db.create_all()

port = int(os.environ.get('PORT', 8080))
if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0', port=port)