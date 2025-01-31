from flask import Blueprint, request, jsonify
from models import Libro
from database import db

libros_bp = Blueprint('libros', __name__)

# Crear un nuevo libro
@libros_bp.route('/libros', methods=['POST'])
def create_libro():
    data = request.get_json()
    new_libro = Libro(
        titulo=data['titulo'],
        isbn=data['isbn'],
        autor=data['autor'],
        editorial=data['editorial'],
        anio_publicacion=data['anio_publicacion'],
        cantidad_total=data['cantidad_total'],
        cantidad_disponible=data['cantidad_disponible'],
        id_categorias=data['id_categorias']
    )
    db.session.add(new_libro)
    db.session.commit()
    return jsonify({'message': 'Libro creado'}), 201

# Obtener todos los libros o buscar por título
@libros_bp.route('/libros', methods=['GET'])
def get_libros():
    query = request.args.get('search', None)  # Obtén el parámetro 'search' de la URL
    if query:
        libros = Libro.query.filter(Libro.titulo.ilike(f"%{query}%")).all()
    else:
        libros = Libro.query.all()

    result = [{
        "id": l.id_libros,
        "titulo": l.titulo,
        "isbn": l.isbn,
        "autor": l.autor,
        "editorial": l.editorial,
        "anio_publicacion": l.anio_publicacion,
        "cantidad_total": l.cantidad_total,
        "cantidad_disponible": l.cantidad_disponible,
        "categoria": l.categoria.nombre if l.categoria else None,  # Relación con categorías
        "etiquetas": [et.etiqueta.nombre for et in l.etiquetas]  # Relación con etiquetas
    } for l in libros]
    return jsonify(result)

# Obtener un libro por ID
@libros_bp.route('/libros/<int:id>', methods=['GET'])
def get_libro(id):
    libro = Libro.query.get_or_404(id)
    return jsonify({
        "id": libro.id_libros,
        "titulo": libro.titulo,
        "isbn": libro.isbn,
        "autor": libro.autor,
        "editorial": libro.editorial,
        "anio_publicacion": libro.anio_publicacion,
        "cantidad_total": libro.cantidad_total,
        "cantidad_disponible": libro.cantidad_disponible,
        "id_categorias": libro.id_categorias
    })

# Actualizar un libro por ID
@libros_bp.route('/libros/<int:id>', methods=['PUT'])
def update_libro(id):
    libro = Libro.query.get_or_404(id)
    data = request.get_json()
    libro.titulo = data['titulo']
    libro.isbn = data['isbn']
    libro.autor = data['autor']
    libro.editorial = data['editorial']
    libro.anio_publicacion = data['anio_publicacion']
    libro.cantidad_total = data['cantidad_total']
    libro.cantidad_disponible = data['cantidad_disponible']
    libro.id_categorias = data['id_categorias']
    db.session.commit()
    return jsonify({"message": "Libro actualizado"})

# Eliminar un libro por ID
@libros_bp.route('/libros/<int:id>', methods=['DELETE'])
def delete_libro(id):
    libro = Libro.query.get_or_404(id)
    db.session.delete(libro)
    db.session.commit()
    return jsonify({"message": "Libro eliminado"})
