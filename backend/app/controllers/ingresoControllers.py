# app/controllers/ingresoController.py
from fastapi import HTTPException
from app.services.ingresoService import (
    get_ingresos_service,
    get_ingreso_service,
    post_ingreso_service,
    put_ingreso_service,
    delete_ingreso_service,
)
from app.schemas.ingreso import IngresoCreate, IngresoUpdate


def get_ingresos_controller(usuario_autenticado: dict) -> list:
    """Controller para GET /ingresos"""
    try:
        return get_ingresos_service()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print(f"Error en get_ingresos_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def get_ingreso_controller(ingreso_id: int, usuario_autenticado: dict) -> dict:
    """Controller para GET /ingresos/{ingreso_id}"""
    try:
        return get_ingreso_service(ingreso_id)
    except ValueError as e:
        error_msg = str(e)
        if "no encontrado" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        print(f"Error en get_ingreso_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def post_ingreso_controller(
    ingreso_data: IngresoCreate, usuario_autenticado: dict
) -> dict:
    """Controller para POST /ingresos

    Recibe el schema IngresoCreate validado
    """
    try:
        return post_ingreso_service(ingreso_data)
    except ValueError as e:
        error_msg = str(e)
        if "usuario" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        print(f"Error en post_ingreso_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def put_ingreso_controller(
    ingreso_id: int, ingreso_data: IngresoUpdate, usuario_autenticado: dict
) -> dict:
    """Controller para PUT /ingresos/{ingreso_id}

    Recibe el schema IngresoUpdate validado
    """
    try:
        return put_ingreso_service(ingreso_id, ingreso_data)
    except ValueError as e:
        error_msg = str(e)
        if "no encontrado" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        print(f"Error en put_ingreso_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def delete_ingreso_controller(ingreso_id: int, usuario_autenticado: dict) -> dict:
    """Controller para DELETE /ingresos/{ingreso_id}"""
    try:
        return delete_ingreso_service(ingreso_id)
    except ValueError as e:
        error_msg = str(e)
        if "no encontrado" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        print(f"Error en delete_ingreso_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
