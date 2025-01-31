from flask import Blueprint, request, jsonify
from models import Bibliotecario
from database import db
from config import Config
import jwt
import datetime
from flask_bcrypt import Bcrypt


bibliotecarios_bp = Blueprint('bibliotecarios', __name__)
bcrypt = Bcrypt()

#22/1/25
@bibliotecarios_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    bibliotecario = Bibliotecario.query.filter_by(email=email).first()
    if bibliotecario and bcrypt.check_password_hash(bibliotecario.password, password):
        token = jwt.encode(
            {
                'id': bibliotecario.id_bibliotecarios,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            },
            Config.SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify({'token': token, 'id': bibliotecario.id_bibliotecarios })    # Incluye el ID en la respuesta
    return jsonify({'message': 'Credenciales incorrectas'}), 401

@bibliotecarios_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_bibliotecario = Bibliotecario(
        nombre=data['nombre'],
        email=data['email'],
        password=hashed_password,
        estado=data['estado']
    )
    db.session.add(new_bibliotecario)
    db.session.commit()
    # Generar token
    token = jwt.encode(
        {
            'id': new_bibliotecario.id_bibliotecarios,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        },
        Config.SECRET_KEY,
        algorithm="HS256"
    )
    return jsonify({'message': 'Usuario registrado correctamente', 'token': token}), 201
#    

@bibliotecarios_bp.route('/bibliotecarios', methods=['POST'])
def create_bibliotecario():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_bibliotecario = Bibliotecario(
        nombre=data['nombre'],
        email=data['email'],
        password=hashed_password,
        estado=data['estado']
    )
    db.session.add(new_bibliotecario)
    db.session.commit()
    return jsonify({'message': 'Bibliotecario creado correctamente'}), 201

@bibliotecarios_bp.route('/bibliotecarios', methods=['GET'])
def get_bibliotecarios():
    bibliotecarios = Bibliotecario.query.all()
    result = [{"id": b.id_bibliotecarios, "nombre": b.nombre, "email": b.email} for b in bibliotecarios]
    return jsonify(result)

@bibliotecarios_bp.route('/bibliotecarios/<int:id>', methods=['GET'])
def get_bibliotecario(id):
    bibliotecario = Bibliotecario.query.get_or_404(id)
    return jsonify({"id": bibliotecario.id_bibliotecarios, "nombre": bibliotecario.nombre, "email": bibliotecario.email})

@bibliotecarios_bp.route('/bibliotecarios/<int:id>', methods=['PUT'])
def update_bibliotecario(id):
    bibliotecario = Bibliotecario.query.get_or_404(id)
    data = request.get_json()
    bibliotecario.nombre = data['nombre']
    bibliotecario.email = data['email']
    if 'password' in data and data['password']:  # Si se proporciona una nueva contraseña
        bibliotecario.password = generate_password_hash(data['password'], method='sha256')    
    bibliotecario.estado = data['estado']
    db.session.commit()
    return jsonify({"message": "Bibliotecario actualizado"})

@bibliotecarios_bp.route('/bibliotecarios/<int:id>', methods=['DELETE'])
def delete_bibliotecario(id):
    bibliotecario = Bibliotecario.query.get_or_404(id)
    db.session.delete(bibliotecario)
    db.session.commit()
    return jsonify({"message": "Bibliotecario eliminado"})
