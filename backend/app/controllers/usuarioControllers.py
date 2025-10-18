# app/controllers/usuarioController.py
from fastapi import HTTPException
from services.usuarioService import (
    get_usuarios,
    get_usuario,
    put_usuario,
    delete_usuario,
)


def get_usuarios_controller() -> list:
    """
    Controller para GET /usuarios

    Responsabilidad:
    - Llamar al servicio
    - Convertir ValueError a HTTPException
    - Retornar respuesta HTTP
    """
    try:
        return get_usuarios()

    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print(f"Error en get_usuarios_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def get_usuario_controller(usuario_id: int) -> dict:
    """
    Controller para GET /usuarios/{usuario_id}

    Convierte errores de negocio a errores HTTP:
    - ValueError → 404 o 400
    """
    try:
        return get_usuario(usuario_id)

    except ValueError as e:
        error_msg = str(e)
        if "no encontrado" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)

    except Exception as e:
        print(f"Error en get_usuario_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def put_usuario_controller(usuario_id: int, datos: dict) -> dict:
    """
    Controller para PUT /usuarios/{usuario_id}

    Recibe datos del usuario y los pasa al servicio.
    El servicio maneja la lógica, el controller maneja HTTP.
    """
    try:
        return put_usuario(usuario_id, datos)

    except ValueError as e:
        error_msg = str(e)

        # Determinar el código HTTP según el error
        if "no encontrado" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        elif "ya está registrado" in error_msg.lower():
            raise HTTPException(status_code=400, detail=error_msg)
        elif "No hay campos" in error_msg:
            raise HTTPException(status_code=400, detail=error_msg)
        elif "No puedes cambiar" in error_msg:
            raise HTTPException(status_code=400, detail=error_msg)

        raise HTTPException(status_code=400, detail=error_msg)

    except Exception as e:
        print(f"Error en put_usuario_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def delete_usuario_controller(usuario_id: int) -> dict:
    """
    Controller para DELETE /usuarios/{usuario_id}
    """
    try:
        return delete_usuario(usuario_id)

    except ValueError as e:
        error_msg = str(e)
        if "no encontrado" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)

    except Exception as e:
        print(f"Error en delete_usuario_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
