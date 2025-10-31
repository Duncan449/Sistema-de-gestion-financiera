# app/controllers/pasivoController.py
# Capa de control que maneja las peticiones HTTP y coordina con los servicios
from fastapi import HTTPException
from app.services.pasivoService import (
    get_pasivos_service,
    get_pasivo_service,
    post_pasivo_service,
    put_pasivo_service,
    delete_pasivo_service,
)
from app.schemas.pasivo import PasivoCreate, PasivoUpdate


def get_pasivos_controller(usuario_autenticado: dict) -> list:
    """
    Controller para GET /pasivos
    Obtiene todos los pasivos del usuario autenticado

    """
    try:
         # Extraer el ID del usuario desde el diccionario de autenticación (viene del JWT)
        usuario_id = usuario_autenticado["usuario_id"]

        return get_pasivos_service(usuario_id)
    except ValueError as e:
        
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print(f"Error en get_pasivos_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def get_pasivo_controller(pasivo_id: int, usuario_autenticado: dict) -> dict:
    """
    Controller para GET /pasivos/{pasivo_id}
    Obtiene un pasivo específico por su ID

    """
    try:
        return get_pasivo_service(pasivo_id)
    except ValueError as e:
        error_msg = str(e)
        if "no encontrado" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        print(f"Error en get_pasivo_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def post_pasivo_controller(
    pasivo_data: PasivoCreate, usuario_autenticado: dict
) -> dict:
    """
    Controller para POST /pasivos
    Crea un nuevo pasivo asociado al usuario autenticado
    Recibe el schema PasivoCreate validado por Pydantic

    """
    try:
        usuario_id = usuario_autenticado["usuario_id"] # Extraer el ID del usuario autenticado

        # Pasar los datos del pasivo y el ID del usuario al service
        return post_pasivo_service(pasivo_data, usuario_id)
    except ValueError as e:
        error_msg = str(e)

        if "usuario" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        print(f"Error en post_pasivo_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def put_pasivo_controller(
    pasivo_id: int, pasivo_data: PasivoUpdate, usuario_autenticado: dict
) -> dict:
    """
    Controller para PUT /pasivos/{pasivo_id}
    Actualiza un pasivo existente
    Recibe el schema PasivoUpdate validado con campos opcionales
    
    """
    try:
            # Extraer el ID del usuario autenticado para verificar permisos
            usuario_id = usuario_autenticado["usuario_id"]
            
            # Llamar al service pasando el ID del pasivo, los datos y el usuario
            return put_pasivo_service(pasivo_id, pasivo_data, usuario_id)
    except ValueError as e:
            error_msg = str(e)
            
            if "no encontrado" in error_msg.lower():
                raise HTTPException(status_code=404, detail=error_msg)
            
            raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
            print(f"Error en put_pasivo_controller: {e}")
            raise HTTPException(status_code=500, detail="Error interno del servidor")


def delete_pasivo_controller(pasivo_id: int, usuario_autenticado: dict) -> dict:
    """
    Controller para DELETE /pasivos/{pasivo_id}
    Elimina un pasivo si pertenece al usuario autenticado

    """
    try:
        # Extraer el ID del usuario autenticado
        usuario_id = usuario_autenticado["usuario_id"]  # Extraer el ID

        # Pasar el ID del pasivo y el ID del usuario al service
        return delete_pasivo_service(pasivo_id, usuario_id)
    except ValueError as e:
        error_msg = str(e)
        
        if "no encontrado" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        print(f"Error en delete_pasivo_controller: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")