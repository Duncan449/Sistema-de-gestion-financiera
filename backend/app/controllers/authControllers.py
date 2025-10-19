# app/controllers/authController.py
from fastapi import HTTPException
from app.services.auth_service import (
    login_usuario,
    registrar_usuario,
    cambiar_contraseña_usuario,
)


def login_controller(email: str, password: str) -> dict:
    """
    Controller para POST /auth/login

    El servicio devuelve el token o lanza ValueError
    El controller convierte eso a HTTP
    """
    try:
        return login_usuario(email, password)

    except ValueError as e:
        error_msg = str(e)

        if "no encontrado" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        elif "incorrecta" in error_msg.lower():
            raise HTTPException(status_code=401, detail=error_msg)

        raise HTTPException(status_code=400, detail=error_msg)

    except Exception as e:
        print(f"Error en login_controller: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor {e}")


def registrar_controller(
    nombre_completo: str, email: str, username: str, password: str
) -> dict:
    """
    Controller para POST /auth/register
    """
    try:
        return registrar_usuario(nombre_completo, email, username, password)

    except ValueError as e:
        error_msg = str(e)

        if "ya está registrado" in error_msg.lower():
            raise HTTPException(status_code=400, detail=error_msg)

        raise HTTPException(status_code=400, detail=error_msg)

    except Exception as e:
        print(f"Error en registrar_controller: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")


def cambiar_contraseña_controller(
    usuario_id: int, contraseña_actual: str, contraseña_nueva: str
) -> dict:
    """
    Controller para POST /auth/cambiar-contraseña
    """
    try:
        return cambiar_contraseña_usuario(
            usuario_id, contraseña_actual, contraseña_nueva
        )

    except ValueError as e:
        error_msg = str(e)

        if "no encontrado" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        elif "incorrecta" in error_msg.lower():
            raise HTTPException(status_code=401, detail=error_msg)

        raise HTTPException(status_code=400, detail=error_msg)

    except Exception as e:
        print(f"Error en cambiar_contraseña_controller: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor {e}")
