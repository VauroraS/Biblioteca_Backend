import pytest
from app import create_app, db
from models import Libro, Categoria, Prestamo

@pytest.fixture
def client():
    """Crea un cliente de prueba con la base de datos de testing."""
    app = create_app(TestingConfig)
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Crea la BD desde cero
            yield client  # Devuelve el cliente de pruebas
            db.session.remove()
            db.drop_all()  # Borra datos después de cada test

def test_registrar_libro(client):
    """Prueba el registro de un libro en la base de datos"""
    nuevo_libro = Libro(
        titulo="El Quijote",
        isbn="1234567890",
        autor="Miguel de Cervantes",
        editorial="Editorial Clásica",
        anio_publicacion=1605,
        cantidad_total=10,
        cantidad_disponible=10
    )

    with client.application.app_context():
        db.session.add(nuevo_libro)
        db.session.commit()

        libro_db = Libro.query.filter_by(titulo="El Quijote").first()
        assert libro_db is not None
        assert libro_db.isbn == "1234567890"

def test_buscar_libro(client):
    """Prueba la búsqueda de un libro"""
    with client.application.app_context():
        libro = Libro(
            titulo="Cien años de soledad",
            isbn="1234567891",
            autor="Gabriel García Márquez",
            editorial="Sudamericana",
            anio_publicacion=1967,
            cantidad_total=5,
            cantidad_disponible=5
        )
        db.session.add(libro)
        db.session.commit()

        response = client.get("/libros?titulo=Cien años de soledad")
        assert response.status_code == 200
        data = response.get_json()
        assert data[0]["titulo"] == "Cien años de soledad"

def test_solicitar_prestamo(client):
    """Prueba la solicitud de un préstamo"""
    with client.application.app_context():
        libro = Libro(
            titulo="1984",
            isbn="1234567892",
            autor="George Orwell",
            editorial="Secker & Warburg",
            anio_publicacion=1949,
            cantidad_total=3,
            cantidad_disponible=3
        )
        db.session.add(libro)
        db.session.commit()

        response = client.post("/prestamos", json={"isbn": "1234567892", "lector_id": 1})
        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "Préstamo registrado con éxito"

