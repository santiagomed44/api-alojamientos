from marshmallow import Schema, fields, validate


class RegistroUsuarioDTO(Schema):
    correo = fields.Email(required=True)
    contrasena = fields.String(
        required=True,
        validate=validate.Length(min=6),
        load_only=True,
    )
    nombre = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
    )
    apellido = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
    )


class LoginUsuarioDTO(Schema):
    correo = fields.Email(required=True)
    contrasena = fields.String(
        required=True,
        load_only=True,
    )