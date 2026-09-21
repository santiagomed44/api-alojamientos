import pytest

from app import create_app, db


@pytest.fixture
def app():
    aplicacion = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SECRET_KEY": "clave-exclusiva-para-tests-1234567890",
            "JWT_EXP_MINUTES": 15,
        }
    )

    with aplicacion.app_context():
        db.create_all()

    yield aplicacion

    with aplicacion.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def token_usuario(client):
    datos_usuario = {
        "correo": "autenticado@example.com",
        "contrasena": "123456",
        "nombre": "Usuario",
        "apellido": "Autenticado",
    }

    respuesta_registro = client.post(
        "/api/v1/usuarios/registro",
        json=datos_usuario,
    )

    assert respuesta_registro.status_code == 201

    respuesta_login = client.post(
        "/api/v1/usuarios/login",
        json={
            "correo": datos_usuario["correo"],
            "contrasena": datos_usuario["contrasena"],
        },
    )

    assert respuesta_login.status_code == 200

    return respuesta_login.get_json()["access_token"]


@pytest.fixture
def headers_autenticados(token_usuario):
    return {
        "Authorization": f"Bearer {token_usuario}",
    }


@pytest.fixture
def token_admin(app, client):
    from app.dominios.usuarios.modelos import Usuario

    datos_usuario = {
        "correo": "admin@example.com",
        "contrasena": "123456",
        "nombre": "Usuario",
        "apellido": "Admin",
    }

    respuesta_registro = client.post(
        "/api/v1/usuarios/registro",
        json=datos_usuario,
    )

    assert respuesta_registro.status_code == 201

    with app.app_context():
        usuario = db.session.scalar(
            db.select(Usuario).where(
                Usuario.correo == datos_usuario["correo"]
            )
        )

        usuario.rol = "admin"
        db.session.commit()

    respuesta_login = client.post(
        "/api/v1/usuarios/login",
        json={
            "correo": datos_usuario["correo"],
            "contrasena": datos_usuario["contrasena"],
        },
    )

    assert respuesta_login.status_code == 200

    return respuesta_login.get_json()["access_token"]


@pytest.fixture
def headers_admin(token_admin):
    return {
        "Authorization": f"Bearer {token_admin}",
    }