# app/seguridad.py

from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, g, request

from app.errores import ErrorAPI


def generar_token(usuario_id):
    """Genera un JWT para el usuario autenticado."""
    ahora = datetime.now(timezone.utc)

    payload = {
        "sub": str(usuario_id),
        "iat": ahora,
        "exp": ahora
        + timedelta(minutes=current_app.config["JWT_EXP_MINUTES"]),
    }

    return jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )


def requiere_token(funcion):
    """Protege un endpoint mediante Bearer Token."""

    @wraps(funcion)
    def envoltura(*args, **kwargs):
        encabezado = request.headers.get("Authorization", "")

        if not encabezado.startswith("Bearer "):
            raise ErrorAPI(
                mensaje="Token de autenticación requerido.",
                status_code=401,
                codigo="token_requerido",
            )

        token = encabezado.split(" ", 1)[1].strip()

        if not token:
            raise ErrorAPI(
                mensaje="Token de autenticación requerido.",
                status_code=401,
                codigo="token_requerido",
            )

        try:
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"],
            )

            usuario_id = int(payload["sub"])

        except jwt.ExpiredSignatureError:
            raise ErrorAPI(
                mensaje="El token ha expirado.",
                status_code=401,
                codigo="token_expirado",
            )

        except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
            raise ErrorAPI(
                mensaje="Token inválido.",
                status_code=401,
                codigo="token_invalido",
            )

        g.usuario_id = usuario_id

        return funcion(*args, **kwargs)

    return envoltura


def requiere_admin(funcion):
    """Permite el acceso únicamente a usuarios con rol admin."""

    @wraps(funcion)
    def envoltura(*args, **kwargs):
        from app.dominios.usuarios.repositorios import UsuarioRepositorio

        usuario = UsuarioRepositorio.obtener_por_id(g.usuario_id)

        if usuario is None:
            raise ErrorAPI(
                mensaje="Usuario no encontrado.",
                status_code=404,
                codigo="usuario_no_encontrado",
            )

        if usuario.rol != "admin":
            raise ErrorAPI(
                mensaje="No tiene permisos para acceder a este recurso.",
                status_code=403,
                codigo="acceso_denegado",
            )

        return funcion(*args, **kwargs)

    return envoltura