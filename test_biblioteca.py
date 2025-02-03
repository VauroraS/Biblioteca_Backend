import pytest
from config import TestingConfig
from app import create_app, db

@pytest.fixture
def client():
    """Crea un cliente de prueba con la base de datos de testing."""
    app = create_app(TestingConfig)
    app.config.update({"TESTING": True})
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Crea las tablas en la BD de prueba
        yield client
        with app.app_context():
            db.drop_all()  # Limpia la BD después de cada test

def test_registrar_libro(client):
    """Prueba el registro de un libro en la biblioteca."""
    response = client.post("/libros", json={
        "titulo": "Libro de Prueba",
        "autor": "Autor Test",
        "isbn": "1234567890",
        "editorial": "Editorial Test",
        "anio_publicacion": 2025,
        "cantidad_total": 10,
        "cantidad_disponible": 10,
        "id_categorias": 2
    })
    assert response.status_code == 201

def test_buscar_libro(client):
    """Prueba la búsqueda de libros."""
    response = client.get("/libros?titulo=Libro de Prueba")
    assert response.status_code == 200
    assert b"Libro de Prueba" in response.data

def test_solicitar_prestamo(client):
    """Prueba la solicitud de préstamo de un libro."""
    response = client.post("/prestamos", json={"libro_id": 1, "lector_id": 1})
    assert response.status_code == 201


