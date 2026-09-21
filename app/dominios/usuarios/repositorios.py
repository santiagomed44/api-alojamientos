# app/dominios/usuarios/repositorios.py

from app import db
from app.dominios.usuarios.modelos import PerfilUsuario, Usuario


class UsuarioRepositorio:
    """Acceso a datos del dominio de usuarios."""

    @staticmethod
    def obtener_por_correo(correo):
        sentencia = db.select(Usuario).where(Usuario.correo == correo)
        return db.session.scalar(sentencia)

    @staticmethod
    def obtener_por_id(usuario_id):
        return db.session.get(Usuario, usuario_id)

    @staticmethod
    def crear(correo, contrasena_hash, nombre, apellido):
        usuario = Usuario(
            correo=correo,
            contrasena=contrasena_hash,
        )

        usuario.perfil = PerfilUsuario(
            nombre=nombre,
            apellido=apellido,
        )

        db.session.add(usuario)
        db.session.commit()

        return usuario

    @staticmethod
    def listar_todos():
        sentencia = db.select(Usuario).order_by(Usuario.id)
        return db.session.scalars(sentencia).all()