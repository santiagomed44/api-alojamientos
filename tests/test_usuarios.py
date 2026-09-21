def test_registro_usuario_correcto(client):
    respuesta = client.post(
        "/api/v1/usuarios/registro",
        json={
            "correo": "usuario@example.com",
            "contrasena": "123456",
            "nombre": "Usuario",
            "apellido": "Prueba",
        },
    )

    assert respuesta.status_code == 201


def test_registro_rechaza_correo_invalido(client):
    respuesta = client.post(
        "/api/v1/usuarios/registro",
        json={
            "correo": "correo-invalido",
            "contrasena": "123456",
            "nombre": "Usuario",
            "apellido": "Prueba",
        },
    )

    assert respuesta.status_code == 400


def test_registro_rechaza_correo_duplicado(client):
    datos = {
        "correo": "duplicado@example.com",
        "contrasena": "123456",
        "nombre": "Usuario",
        "apellido": "Duplicado",
    }

    primera_respuesta = client.post(
        "/api/v1/usuarios/registro",
        json=datos,
    )

    segunda_respuesta = client.post(
        "/api/v1/usuarios/registro",
        json=datos,
    )

    assert primera_respuesta.status_code == 201
    assert segunda_respuesta.status_code == 409


def test_login_valido_retorna_access_token(client):
    datos_registro = {
        "correo": "login@example.com",
        "contrasena": "123456",
        "nombre": "Usuario",
        "apellido": "Login",
    }

    respuesta_registro = client.post(
        "/api/v1/usuarios/registro",
        json=datos_registro,
    )

    assert respuesta_registro.status_code == 201

    respuesta = client.post(
        "/api/v1/usuarios/login",
        json={
            "correo": "login@example.com",
            "contrasena": "123456",
        },
    )

    assert respuesta.status_code == 200

    datos = respuesta.get_json()

    assert "access_token" in datos
    assert datos["access_token"]


def test_login_invalido_retorna_401(client):
    datos_registro = {
        "correo": "login-invalido@example.com",
        "contrasena": "123456",
        "nombre": "Usuario",
        "apellido": "Login",
    }

    respuesta_registro = client.post(
        "/api/v1/usuarios/registro",
        json=datos_registro,
    )

    assert respuesta_registro.status_code == 201

    respuesta = client.post(
        "/api/v1/usuarios/login",
        json={
            "correo": "login-invalido@example.com",
            "contrasena": "contrasena-incorrecta",
        },
    )

    assert respuesta.status_code == 401


def test_perfil_sin_token_retorna_401(client):
    respuesta = client.get(
        "/api/v1/usuarios/perfil",
    )

    assert respuesta.status_code == 401


def test_perfil_con_token_retorna_200(
    client,
    headers_autenticados,
):
    respuesta = client.get(
        "/api/v1/usuarios/perfil",
        headers=headers_autenticados,
    )

    assert respuesta.status_code == 200


def test_usuario_normal_no_puede_listar_usuarios(
    client,
    headers_autenticados,
):
    respuesta = client.get(
        "/api/v1/admin/usuarios",
        headers=headers_autenticados,
    )

    assert respuesta.status_code == 403


def test_admin_puede_listar_usuarios(
    client,
    headers_admin,
):
    respuesta = client.get(
        "/api/v1/admin/usuarios",
        headers=headers_admin,
    )

    assert respuesta.status_code == 200