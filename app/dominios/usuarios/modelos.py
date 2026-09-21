from datetime import datetime, timezone

from app import db


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(255), unique=True, nullable=False, index=True)
    contrasena = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default="usuario")
    creado_en = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    perfil = db.relationship(
        "PerfilUsuario",
        back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan",
    )


class PerfilUsuario(db.Model):
    __tablename__ = "perfiles"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        unique=True,
        nullable=False,
    )
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)

    usuario = db.relationship(
        "Usuario",
        back_populates="perfil",
    )