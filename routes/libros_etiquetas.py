from flask import Blueprint, request, jsonify
from models import LibroEtiqueta
from database import db

libros_etiquetas_bp = Blueprint('libros_etiquetas', __name__)

# Crear una nueva relación libro-etiqueta
@libros_etiquetas_bp.route('/libros_etiquetas', methods=['POST'])
def create_libro_etiqueta():
    data = request.get_json()
    new_relacion = LibroEtiqueta(id_libros=data['id_libros'], id_etiquetas=data['id_etiquetas'])
    db.session.add(new_relacion)
    db.session.commit()
    return jsonify({'message': 'Relación libro-etiqueta creada'}), 201

# Obtener todas las relaciones libro-etiqueta
@libros_etiquetas_bp.route('/libros_etiquetas', methods=['GET'])
def get_libros_etiquetas():
    relaciones = LibroEtiqueta.query.all()
    result = [{
        "id": r.id_libros_etiquetas,
        "id_libros": r.id_libros,
        "id_etiquetas": r.id_etiquetas
    } for r in relaciones]
    return jsonify(result)
