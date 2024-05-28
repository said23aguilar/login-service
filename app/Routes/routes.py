from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from Models.models import Usuario
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
import bcrypt
from flask_bcrypt import Bcrypt
from database import db

blue_print = Blueprint('app', __name__)


# Ruta de Inicio
@blue_print.route('/', methods=['GET'])
def holamundo():
    return jsonify(respuesta='SAP LOGIN')


# Registro de Usuario
@cross_origin()
@blue_print.route('/auth/registrar', methods=['POST'])
def registrar_usuario():
    try:
        # Obtenemos los datos de usuario
        usuario = request.json.get('usuario')
        password = request.json.get('password')
        nombre = request.json.get('nombre')
        tipo = request.json.get('tipo')

        if not usuario or not password or not nombre or not tipo :
            return jsonify(respuesta='Campos Invalidos'), 400

        # Consultar la BD
        existe_usuario = Usuario.query.filter_by(usuario=usuario).first()
        if existe_usuario:
            return jsonify(respuesta='Usuario ya Existe'), 400

        # Encriptamos la password
        password_encriptada = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        

        # Creamos el modelo a guardar en BD
        nuevo_usuario = Usuario(
            usuario, password_encriptada, nombre, tipo)

        print(usuario, password, nombre, tipo)

        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify(respuesta='Usuario Creado Exitosamente'), 200
    except Exception as e:
        return jsonify(error = e), 500

# Ruta para Iniciar Sesion

@cross_origin()
@blue_print.route('/auth/login', methods=['POST'])
def iniciar_sesion():
    try:
        # Obtenemos los datos de usuario
        usuario = request.json.get('usuario')
        password = request.json.get('password')

        if not usuario or not password:
            return jsonify(respuesta='Campos Invalidos'), 400

        # Consultar la BD
        user = Usuario.query.filter_by(usuario=usuario).first()

        if not user:
            return jsonify(respuesta='Usuario No Encontrado'), 404

        password_valid = bcrypt.checkpw(password.encode(
            'utf-8'), user.password.encode('utf-8'))

        # Validamos Password
        if password_valid:
            token = create_access_token(identity=user.id)
            return jsonify({'token': token, 'id': user.id, 'usuario': user.usuario, 'nombre': user.nombre, 'tipo': user.tipo}), 200
        return jsonify(respuesta='Clave o Usuario Incorrecto'), 404

    except Exception as e:
        return jsonify(respuesta= e), 500

@cross_origin()
@blue_print.route('/auth/perfil', methods=['GET'])
@jwt_required()
def perfil():
    current_user_id = get_jwt_identity()
    user = Usuario.query.get(current_user_id)

    return jsonify({'id': user.id, 'usuario': user.usuario, 'nombre': user.nombre, 'tipo': user.tipo}), 200
