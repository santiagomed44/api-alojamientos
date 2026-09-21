# API Alojamientos

API REST desarrollada con Flask como proyecto académico de Backend.

La versión actual integra los resultados de los Sprint 1 y Sprint 2 e incluye configuración del proyecto, conexión con MySQL, migraciones, registro de usuarios, autenticación mediante JWT, autorización por roles, pruebas automatizadas y pruebas manuales con Postman.

## Funcionalidades implementadas

- App Factory con Flask.
- Configuración mediante variables de entorno.
- Conexión a MySQL mediante SQLAlchemy.
- Migraciones con Flask-Migrate y Alembic.
- Configuración de CORS.
- Endpoint de salud de la API.
- Dominio de usuarios organizado por módulos.
- Registro de usuarios.
- Validación de datos con Marshmallow.
- Contraseñas almacenadas mediante hash.
- Inicio de sesión.
- Generación y validación de JWT.
- Autenticación mediante Bearer Token.
- Roles `usuario` y `admin`.
- Endpoint de perfil protegido.
- Endpoint administrativo protegido por rol.
- Manejo centralizado de errores HTTP.
- Pruebas automatizadas con pytest.
- Colecciones y environments de Postman.

## Tecnologías principales

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-CORS
- MySQL
- PyMySQL
- Marshmallow
- PyJWT
- pytest
- Postman
- Git y GitHub

## Estructura general

```text
api-alojamientos/
├── app/
│   ├── dominios/
│   │   └── usuarios/
│   ├── __init__.py
│   ├── config.py
│   ├── errores.py
│   └── seguridad.py
├── docs/
│   └── postman/
├── migrations/
├── scripts/
├── tests/
├── .env.example
├── .gitignore
├── app.py
├── pytest.ini
├── README.md
└── requirements.txt
```

## Requisitos previos

Para ejecutar el proyecto se requiere:

- Python 3
- MySQL
- Git
- Postman, opcional para las pruebas manuales

## Instalación

Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd api-alojamientos
```

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activarlo en Windows con Git Bash:

```bash
source .venv/Scripts/activate
```

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Configuración de variables de entorno

Crear un archivo `.env` a partir de `.env.example`.

En Git Bash:

```bash
cp .env.example .env
```

Configurar las variables de acuerdo con la instalación local de MySQL:

```env
DB_USER=root
DB_PASSWORD=contraseña_mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=alojamientos_db

CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

SECRET_KEY=clave-segura-de-al-menos-32-caracteres
JWT_EXP_MINUTES=15
```

> El archivo `.env` contiene información sensible y no debe almacenarse en Git.

## Creación de la base de datos

Crear la base de datos en MySQL:

```sql
CREATE DATABASE alojamientos_db;
```

El puerto de MySQL puede variar según la instalación local. Debe coincidir con el valor de `DB_PORT` configurado en `.env`.

## Verificación de la conexión MySQL

Ejecutar:

```bash
python -m scripts.verificar_mysql
```

Una conexión correcta mostrará información similar a:

```text
Conexión MySQL correcta
Base de datos: alojamientos_db
```

## Migraciones

Aplicar las migraciones existentes:

```bash
flask --app app.py db upgrade
```

Consultar la migración actualmente aplicada:

```bash
flask --app app.py db current
```

Verificar si existen cambios de modelo pendientes:

```bash
flask --app app.py db check
```

## Ejecución de la API

Iniciar el servidor de desarrollo:

```bash
flask --app app.py run --debug
```

La API estará disponible normalmente en:

```text
http://127.0.0.1:5000
```

## Endpoints principales

### Estado de la API

```http
GET /health
```

Respuesta esperada:

```json
{
  "service": "alojamientos-api",
  "status": "ok",
  "version": "v1"
}
```

### Registro de usuario

```http
POST /api/v1/usuarios/registro
```

Ejemplo:

```json
{
  "correo": "usuario@example.com",
  "contrasena": "123456",
  "nombre": "Usuario",
  "apellido": "Prueba"
}
```

Respuesta exitosa:

```text
201 Created
```

Casos principales:

- `201`: usuario creado.
- `400`: datos inválidos.
- `409`: correo ya registrado.

### Inicio de sesión

```http
POST /api/v1/usuarios/login
```

Ejemplo:

```json
{
  "correo": "usuario@example.com",
  "contrasena": "123456"
}
```

Respuesta exitosa:

```json
{
  "access_token": "..."
}
```

Casos principales:

- `200`: autenticación correcta.
- `401`: credenciales incorrectas.

## Autenticación mediante JWT

Los endpoints protegidos utilizan:

```http
Authorization: Bearer <access_token>
```

### Perfil del usuario autenticado

```http
GET /api/v1/usuarios/perfil
```

Casos principales:

- `200`: token válido.
- `401`: token ausente, inválido o expirado.

## Autorización por roles

### Listado administrativo de usuarios

```http
GET /api/v1/admin/usuarios
```

Este recurso requiere:

- JWT válido.
- Usuario con rol `admin`.

Casos principales:

- `200`: administrador autorizado.
- `401`: usuario no autenticado.
- `403`: usuario autenticado sin permisos administrativos.

## Pruebas automatizadas

Ejecutar:

```bash
pytest -q
```

La versión correspondiente a Sprint 1 + Sprint 2 dispone de pruebas automatizadas para:

- Health check.
- Registro correcto.
- Validación de correo.
- Correo duplicado.
- Login correcto.
- Login incorrecto.
- Acceso a perfil con y sin token.
- Autorización administrativa según el rol.

Todas las pruebas deben finalizar satisfactoriamente antes de entregar una nueva versión.

## Postman

Las evidencias y configuraciones de pruebas manuales se encuentran en:

```text
docs/postman/
```

Incluyen:

```text
Alojamientos-API-Sprint-01.postman_collection.json
Alojamientos-API-Sprint-01.postman_environment.json
Alojamientos-API-Sprint-02.postman_collection.json
Alojamientos-API-Sprint-02.postman_environment.json
```

Para Sprint 2, el Environment incluye las variables:

```text
baseUrl
token_usuario
token_admin
```

Los tokens se entregan vacíos por razones de seguridad. Deben obtenerse mediante el endpoint de login y configurarse localmente en Postman.

## Seguridad

No deben almacenarse en el repositorio:

- Archivo `.env`.
- Contraseñas reales.
- JWT activos.
- Claves privadas.
- `SECRET_KEY` utilizada en un entorno real.

El repositorio contiene únicamente `.env.example` como plantilla de configuración.

## Sprints integrados

### Sprint 1

Fundamentos del proyecto:

- Flask.
- Configuración.
- MySQL.
- SQLAlchemy.
- Migraciones.
- CORS.
- Health check.
- Pruebas iniciales.

### Sprint 2

Autenticación y autorización:

- Dominio de usuarios.
- Registro.
- Validación.
- Hash de contraseñas.
- Login.
- JWT.
- Bearer Token.
- Perfil autenticado.
- Roles.
- Endpoint administrativo.
- Pruebas automatizadas.
- Pruebas Postman.

## Estado de la entrega

La rama `main` corresponde a la versión integrada de Sprint 1 y Sprint 2 y constituye la base para los siguientes incrementos del proyecto.