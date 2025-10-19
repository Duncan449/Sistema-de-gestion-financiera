# app/controllers/egresoController.py
from fastapi import HTTPException
from app.services.egresoService import (
    get_egresos_service,
    get_egreso_service,
    post_egreso_service,
    put_egreso_service,
    delete_egreso_service,
)
from app.schemas.egreso import EgresoCreate, EgresoUpdate


def get_egresos_controller(usuario_autenticado: dict) -> list:
    """Controller para GET /egresos"""
    try:
        return get_egresos_service()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print(f"Error en get_egresos_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def get_egreso_controller(egreso_id: int, usuario_autenticado: dict) -> dict:
    """Controller para GET /egresos/{egreso_id}"""
    try:
        return get_egreso_service(egreso_id)
    except ValueError as e:
        error_msg = str(e)
        if "no encontrado" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        print(f"Error en get_egreso_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def post_egreso_controller(
    egreso_data: EgresoCreate, usuario_autenticado: dict
) -> dict:
    """Controller para POST /egresos"""
    try:
        return post_egreso_service(egreso_data)
    except ValueError as e:
        error_msg = str(e)
        if "usuario" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        print(f"Error en post_egreso_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def put_egreso_controller(
    egreso_id: int, egreso_data: EgresoUpdate, usuario_autenticado: dict
) -> dict:
    """Controller para PUT /egresos/{egreso_id}"""
    try:
        return put_egreso_service(egreso_id, egreso_data)
    except ValueError as e:
        error_msg = str(e)
        if "no encontrado" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        print(f"Error en put_egreso_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def delete_egreso_controller(egreso_id: int, usuario_autenticado: dict) -> dict:
    """Controller para DELETE /egresos/{egreso_id}"""
    try:
        return delete_egreso_service(egreso_id)
    except ValueError as e:
        error_msg = str(e)
        if "no encontrado" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        print(f"Error en delete_egreso_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
