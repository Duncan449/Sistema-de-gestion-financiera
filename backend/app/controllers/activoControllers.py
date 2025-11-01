# app/controllers/activoController.py
from fastapi import HTTPException
from app.services.activoService import (
    get_activos_service,
    get_activo_service,
    post_activo_service,
    put_activo_service,
    delete_activo_service,
)
from app.schemas.activo import ActivoCreate, ActivoUpdate


def get_activos_controller(usuario_autenticado: dict) -> list:
    """Controller para GET /activos"""
    try:
        return get_activos_service(usuario_autenticado["usuario_id"])
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print(f"Error en get_activos_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def get_activo_controller(activo_id: int, usuario_autenticado: dict) -> dict:
    """Controller para GET /activos/{activo_id}"""
    try:
        return get_activo_service(activo_id)
    except ValueError as e:
        error_msg = str(e)
        if "no encontrado" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        print(f"Error en get_activo_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def post_activo_controller(
    activo_data: ActivoCreate, usuario_autenticado: dict
) -> dict:
    """Controller para POST /activos

    Recibe el schema ActivoCreate validado
    """
    try:
        return post_activo_service(activo_data, usuario_autenticado["usuario_id"])
    except ValueError as e:
        error_msg = str(e)
        if "usuario" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        print(f"Error en post_activo_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def put_activo_controller(
    activo_id: int, activo_data: ActivoUpdate, usuario_autenticado: dict
) -> dict:
    """Controller para PUT /activos/{activo_id}

    Recibe el schema ActivoUpdate validado
    """
    try:
        return put_activo_service(
            activo_id, activo_data, usuario_autenticado["usuario_id"]
        )
    except ValueError as e:
        error_msg = str(e)
        if "no encontrado" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        print(f"Error en put_activo_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def delete_activo_controller(activo_id: int, usuario_autenticado: dict) -> dict:
    """Controller para DELETE /activos/{activo_id}"""
    try:
        return delete_activo_service(activo_id, usuario_autenticado["usuario_id"])
    except ValueError as e:
        error_msg = str(e)
        if "no encontrado" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        print(f"Error en delete_activo_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
