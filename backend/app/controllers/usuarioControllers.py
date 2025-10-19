# app/controllers/usuarioController.py
from fastapi import HTTPException
from app.services.usuarioService import (
    get_usuarios,
    get_usuario,
    put_usuario,
    delete_usuario,
)


def get_usuarios_controller(usuario_autenticado: dict) -> list:
    """
    Controller para GET /usuarios

    Responsabilidad:
    - Llamar al servicio
    - Convertir ValueError a HTTPException
    - Retornar respuesta HTTP
    """
    try:
        print(f"Usuario autenticado: {usuario_autenticado['email']}")

        return get_usuarios()

    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print(f"Error en get_usuarios_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def get_usuario_controller(usuario_id: int, usuario_autenticado: dict) -> dict:
    """
    Controller para GET /usuarios/{usuario_id}

    Convierte errores de negocio a errores HTTP:
    - ValueError → 404 o 400
    """
    try:
        # Ejemplo: Solo dejar que los usuarios vean su propio perfil
        # if usuario_autenticado["usuario_id"] != usuario_id:
        #     raise HTTPException(status_code=403, detail="No tienes permiso para ver este usuario")
        return get_usuario(usuario_id)

    except ValueError as e:
        error_msg = str(e)
        if "no encontrado" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)

    except Exception as e:
        print(f"Error en get_usuario_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def put_usuario_controller(
    usuario_id: int, datos: dict, usuario_autenticado: dict
) -> dict:
    """
    Controller para PUT /usuarios/{usuario_id}

    Recibe datos del usuario y los pasa al servicio.
    El servicio maneja la lógica, el controller maneja HTTP.
    Seguridad: un usuario solo puede actualizar su propio perfil
    """
    try:
        # Validar que el usuario solo pueda editar su propio perfil
        if usuario_autenticado["usuario_id"] != usuario_id:
            raise HTTPException(
                status_code=403, detail="No tienes permiso para editar este usuario"
            )

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


def delete_usuario_controller(usuario_id: int, usuario_autenticado: dict) -> dict:
    """
    Controller para DELETE /usuarios/{usuario_id}

    Seguridad: Un usuario solo puede eliminar su propia cuenta

    """
    try:

        # Validar que el usuario solo pueda eliminar su propia cuenta
        if usuario_autenticado["usuario_id"] != usuario_id:
            raise HTTPException(
                status_code=403, detail="No tienes permiso para eliminar este usuario"
            )

        return delete_usuario(usuario_id)

    except ValueError as e:
        error_msg = str(e)
        if "no encontrado" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)

    except Exception as e:
        print(f"Error en delete_usuario_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
