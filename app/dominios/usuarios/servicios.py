# app/dominios/usuarios/servicios.py

from werkzeug.security import check_password_hash, generate_password_hash

from app.dominios.usuarios.repositorios import UsuarioRepositorio
from app.errores import ErrorAPI
from app.seguridad import generar_token


class UsuarioServicio:
    """Reglas de negocio relacionadas con usuarios."""

    @staticmethod
    def registrar(datos):
        correo = datos["correo"].strip().lower()

        usuario_existente = UsuarioRepositorio.obtener_por_correo(correo)

        if usuario_existente:
            raise ErrorAPI(
                mensaje="El correo ya se encuentra registrado.",
                status_code=409,
                codigo="correo_duplicado",
            )

        contrasena_hash = generate_password_hash(datos["contrasena"])

        usuario = UsuarioRepositorio.crear(
            correo=correo,
            contrasena_hash=contrasena_hash,
            nombre=datos["nombre"].strip(),
            apellido=datos["apellido"].strip(),
        )

        return {
            "id": usuario.id,
            "correo": usuario.correo,
            "rol": usuario.rol,
            "perfil": {
                "nombre": usuario.perfil.nombre,
                "apellido": usuario.perfil.apellido,
            },
        }

    @staticmethod
    def login(datos):
        correo = datos["correo"].strip().lower()

        usuario = UsuarioRepositorio.obtener_por_correo(correo)

        if usuario is None:
            raise ErrorAPI(
                mensaje="Correo o contraseña incorrectos.",
                status_code=401,
                codigo="credenciales_invalidas",
            )

        if not check_password_hash(
            usuario.contrasena,
            datos["contrasena"],
        ):
            raise ErrorAPI(
                mensaje="Correo o contraseña incorrectos.",
                status_code=401,
                codigo="credenciales_invalidas",
            )

        access_token = generar_token(usuario.id)

        return {
            "access_token": access_token,
        }

    @staticmethod
    def obtener_perfil(usuario_id):
        usuario = UsuarioRepositorio.obtener_por_id(usuario_id)

        if usuario is None:
            raise ErrorAPI(
                mensaje="Usuario no encontrado.",
                status_code=404,
                codigo="usuario_no_encontrado",
            )

        return {
            "id": usuario.id,
            "correo": usuario.correo,
            "rol": usuario.rol,
            "perfil": {
                "nombre": usuario.perfil.nombre,
                "apellido": usuario.perfil.apellido,
            },
        }

    @staticmethod
    def listar_usuarios():
        usuarios = UsuarioRepositorio.listar_todos()

        return [
            {
                "id": usuario.id,
                "correo": usuario.correo,
                "rol": usuario.rol,
                "perfil": {
                    "nombre": usuario.perfil.nombre,
                    "apellido": usuario.perfil.apellido,
                },
            }
            for usuario in usuarios
        ]