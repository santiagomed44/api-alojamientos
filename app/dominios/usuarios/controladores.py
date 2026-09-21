from flask import Blueprint, g, jsonify, request

from app.dominios.usuarios.dtos import LoginUsuarioDTO, RegistroUsuarioDTO
from app.dominios.usuarios.servicios import UsuarioServicio
from app.seguridad import requiere_admin, requiere_token


usuarios_bp = Blueprint("usuarios", __name__)
admin_bp = Blueprint("admin", __name__)


@usuarios_bp.post("/registro")
def registrar_usuario():
    datos_entrada = request.get_json(silent=True) or {}

    datos_validos = RegistroUsuarioDTO().load(datos_entrada)

    usuario = UsuarioServicio.registrar(datos_validos)

    return jsonify(
        {
            "mensaje": "Usuario registrado correctamente.",
            "usuario": usuario,
        }
    ), 201


@usuarios_bp.post("/login")
def login_usuario():
    datos_entrada = request.get_json(silent=True) or {}

    datos_validos = LoginUsuarioDTO().load(datos_entrada)

    resultado = UsuarioServicio.login(datos_validos)

    return jsonify(resultado), 200


@usuarios_bp.get("/perfil")
@requiere_token
def obtener_perfil():
    perfil = UsuarioServicio.obtener_perfil(g.usuario_id)

    return jsonify(perfil), 200


@admin_bp.get("/usuarios")
@requiere_token
@requiere_admin
def listar_usuarios():
    usuarios = UsuarioServicio.listar_usuarios()

    return jsonify(
        {
            "usuarios": usuarios,
        }
    ), 200