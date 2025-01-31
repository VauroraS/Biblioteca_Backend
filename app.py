from flask import Flask, jsonify, request
from flask_cors import CORS
from database import db
from routes.bibliotecarios import bibliotecarios_bp
from routes.lectores import lectores_bp
from routes.libros import libros_bp
from routes.prestamos import prestamos_bp
from routes.reserva import reservas_bp
from routes.devolucion import devoluciones_bp
from routes.etiquetas import etiquetas_bp
from routes.libros_etiquetas import libros_etiquetas_bp
from routes.categoria import categorias_bp
from config import Config
import jwt
from functools import wraps
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_object(Config)

CORS(app)

db.init_app(app)
migrate = Migrate(app, db)

# Registrar Blueprints
app.register_blueprint(bibliotecarios_bp)
app.register_blueprint(lectores_bp)
app.register_blueprint(libros_bp)
app.register_blueprint(prestamos_bp)
app.register_blueprint(reservas_bp)
app.register_blueprint(devoluciones_bp)
app.register_blueprint(etiquetas_bp)
app.register_blueprint(libros_etiquetas_bp)
app.register_blueprint(categorias_bp)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token faltante'}), 403
        try:
            jwt.decode(token.split(" ")[1], Config.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 403
        return f(*args, **kwargs)
    return decorated

if __name__ == '__main__':
    app.run(debug=True)

