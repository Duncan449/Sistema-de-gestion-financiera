# Lógica de autenticación
# app/services/auth_service.py
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from pony.orm import db_session
from app.models.usuario import Usuario
import os
from dotenv import load_dotenv
from pony.orm import commit
from fastapi.security import HTTPBearer
from starlette.requests import Request


load_dotenv()

# ========== CONFIGURACIÓN ==========

# Contexto para hash de contraseñas
# bcrypt es más seguro que otros métodos
pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)  # Básicamente creamos nuestra "máquina de hashear"

# Clave secreta para firmar JWT (IMPORTANTE: cambiar en producción)
SECRET_KEY = os.getenv(
    "SECRET_KEY", "tu-clave-secreta-super-segura-cambiar-en-produccion"
)  # Funciona como un sello de autenticidad


# Duración del token (en minutos)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Algoritmo JWT
ALGORITHM = "HS256"  # Es el algoritmo estándar para firmar JWT

security = HTTPBearer()

# ========== FUNCIONES DE HASH ==========


def hash_password(password: str) -> str:
    """
    Convierte una contraseña en un hash seguro usando bcrypt.

    ¿Por qué hashear? Porque si alguien accede a la BD, no obtendrá la contraseña real.

    No confundir Hashear con cifrar.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica que una contraseña coincida con su hash.

    ¿Por qué no comparar directamente?
    - No puedes desencriptar un hash
    - Debes hashear la contraseña del usuario y compararla. Se usa el Salt para eso.

    """
    return pwd_context.verify(plain_password, hashed_password)


# ========== FUNCIONES JWT ==========


def create_access_token(usuario_id: int, email: str) -> str:
    """
    Crea un JWT token con información del usuario.

    ¿Qué contiene el token?
    - usuario_id: ID del usuario (para identificarlo)
    - email: Email del usuario (información adicional)
    - exp: Fecha de expiración (token válido solo 30 minutos)
    - iat: Fecha de creación

    El token se firma con SECRET_KEY, así que cualquier modificación
    lo invalida automáticamente.

    Estructura de JWT:
    header.payload.signature
    """
    # Calcular tiempo de expiración
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Datos que irán en el token -> El "Payload" o "Carga útil"
    to_encode = {
        "usuario_id": usuario_id,
        "email": email,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }

    # Codificar y firmar el token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verifica que un token JWT sea válido y devuelve su contenido.

    ¿Qué ocurre aquí?
    1. Intenta decodificar el token con la SECRET_KEY
    2. Si alguien modificó el token, la firma no coincide → error
    3. Si el token expiró → error
    4. Si todo es válido → devuelve los datos del token

    """
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )  # Decodifica el token
        usuario_id: int = payload.get(
            "usuario_id"
        )  # Extrae los datos del token decodificado
        email: str = payload.get("email")

        if usuario_id is None or email is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        return {"usuario_id": usuario_id, "email": email}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


# ========== FUNCIÓN DE LOGIN ==========


@db_session
def login_usuario(email: str, password: str) -> dict:
    """
    Autentica un usuario y devuelve un JWT token.

    Proceso:
    1. Buscar el usuario por email en la BD
    2. Verificar que la contraseña coincida con el hash
    3. Si todo es correcto, crear y devolver un token JWT
    """
    try:
        usuario = Usuario.get(email=email)

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="No se encontró un usuario con ese correo electrónico",
            )
        # Verificar contraseña
        if not verify_password(password, usuario.password):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")

        # Crear token JWT
        token = create_access_token(usuario.id, usuario.email)

        return {
            "access_token": token,
            "token_type": "bearer",
            "usuario_id": usuario.id,
            "email": usuario.email,
            "nombre_completo": usuario.nombre_completo,
        }  # Devuelve el token e info del usuario

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en login_usuario: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== FUNCIÓN PARA REGISTRAR USUARIO CON HASH ==========


@db_session
def registrar_usuario(
    nombre_completo: str, email: str, username: str, password: str
) -> dict:
    """
    Registra un nuevo usuario con contraseña hasheada.

    """
    try:

        # Verificar si ya existe
        if Usuario.exists(email=email):
            raise HTTPException(status_code=400, detail="El email ya está registrado")

        if Usuario.exists(username=username):
            raise HTTPException(
                status_code=400, detail="El username ya está registrado"
            )

        # Hashear contraseña
        password_hasheada = hash_password(password)

        # Crear usuario
        nuevo_usuario = Usuario(
            nombre_completo=nombre_completo,
            email=email,
            username=username,
            password=password_hasheada,  # ← Guardar hash, no la contraseña
        )

        commit()

        return {
            "id": nuevo_usuario.id,
            "nombre_completo": nuevo_usuario.nombre_completo,
            "email": nuevo_usuario.email,
            "username": nuevo_usuario.username,
            "mensaje": "Usuario registrado correctamente",
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en registrar_usuario: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@db_session
def cambiar_contraseña_usuario(
    usuario_id: int, contraseña_actual: str, contraseña_nueva: str
) -> dict:
    """
    Permite que un usuario cambie su contraseña.

    Proceso:
    1. Buscar el usuario por ID
    2. Verificar que la contraseña actual sea correcta
    3. Hashear la nueva contraseña
    4. Guardarla en la BD
    """
    try:
        # Buscar usuario
        usuario = Usuario.get(id=usuario_id)

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Verificar que la contraseña actual sea correcta
        if not verify_password(contraseña_actual, usuario.password):
            raise HTTPException(status_code=401, detail="Contraseña actual incorrecta")

        # Hashear la nueva contraseña
        nueva_password_hasheada = hash_password(contraseña_nueva)

        # Actualizar en BD
        usuario.password = nueva_password_hasheada
        commit()

        return {
            "mensaje": "Contraseña cambiada correctamente",
            "usuario_id": usuario_id,
            "email": usuario.email,
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al cambiar_contraseña_usuario: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== FUNCIONES PARA VALIDACIÓN DE TOKENS ==========


def obtener_usuario_del_token(token: str) -> dict:
    """
    Valida un JWT token y devuelve los datos del usuario.
    """
    try:
        datos_token = verify_token(token)
        return datos_token

    except Exception as e:
        raise ValueError(f"Token inválido: {str(e)}")


# Dependency de FastAPI para proteger rutas
def obtener_usuario_autenticado(request: Request) -> dict:
    """
    Dependency de FastAPI que valida el token en cada request.

    Uso en rutas:
    @router.get("/perfil")
    def obtener_perfil(usuario: dict = Depends(obtener_usuario_autenticado)):
        return {"mensaje": f"Hola {usuario['email']}"}

    Automaticamente:
    1. Extrae el token del header Authorization: Bearer {token}
    2. Lo valida
    3. Si es válido, pasa los datos del usuario al endpoint
    4. Si no, devuelve 403 Forbidden
    """
    try:
        # Obtener el token del header Authorization
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=403, detail="Token no proporcionado")

        token = auth_header.replace("Bearer ", "")
        return obtener_usuario_del_token(token)

    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=403, detail="Token inválido o expirado")
