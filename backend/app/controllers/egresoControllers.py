# app/controllers/egresoControllers.py
from typing import List
from fastapi import HTTPException
from pony.orm import db_session, commit, select
from app.models.egreso import Egreso
from app.schemas.egreso import EgresoCreate, EgresoUpdate
from app.models.usuario import Usuario

# GET EGRESOS - Devuelve la lista de egresos
@db_session
def get_egresos() -> List[dict]:
    """Obtiene todos los egresos"""
    try:
        # Usar query más directa
        egresos_query = Egreso.select().order_by(Egreso.id)

        resultado = []
        for egreso in egresos_query:
            resultado.append(
                {
                    "id": egreso.id,
                    "monto": egreso.monto,
                    "categoria": egreso.categoria,
                    "fecha": egreso.fecha,
                    "fk_usuarios": egreso.fk_usuarios.id  # Extraer el ID del usuario
                }
            )

        return resultado

    except Exception as e:
        print(f"❌ Error en get_egresos: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

# GET EGRESO - Obtener un egreso por ID
@db_session
def get_egreso(egreso_id: int) -> dict:
    """
    Obtiene un egreso específico por su ID
    """
    try:
        egreso = Egreso.get(id=egreso_id)

        if not egreso:
            raise HTTPException(status_code=404, detail="Egreso no encontrado")

        return {
            "id": egreso.id,
            "monto": egreso.monto,
            "categoria": egreso.categoria,
            "fecha": egreso.fecha,
            "fk_usuarios": egreso.fk_usuarios.id  # Extraer el ID del usuario
        }
    except HTTPException:
        raise
    except Exception as e:
        print("❌ Error en get_egreso:", e)
        raise HTTPException(
            status_code=500, detail=f"Error al obtener el egreso: {str(e)}"
        )
    

# POST EGRESO - Permite crear un egreso
@db_session
def post_egreso(egreso: EgresoCreate):
    """Crea un nuevo egreso en la base de datos"""
    try:
        # Validación adicional del monto
        if egreso.monto <= 0:
            raise HTTPException(status_code=400, detail="El monto debe ser mayor a 0")

        # Obtener el usuario
        usuario = Usuario.get(id=egreso.fk_usuarios)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Crear el nuevo egreso
        nuevo_egreso = Egreso(
            monto=egreso.monto,
            categoria=egreso.categoria,
            fecha=egreso.fecha,
            fk_usuarios=usuario  # Pasar el objeto usuario, no un ID
        )

        commit()

        return {
            "id": nuevo_egreso.id,
            "monto": nuevo_egreso.monto,
            "categoria": nuevo_egreso.categoria,
            "fecha": nuevo_egreso.fecha,
            "fk_usuarios": nuevo_egreso.fk_usuarios.id
        }

    except HTTPException:
        raise
    except Exception as e:
        print("❌ Error en post_egreso:", e)
        raise HTTPException(
            status_code=400, detail=f"Error al crear el egreso: {str(e)}"
        )
    

# PUT EGRESO - Permite modificar un egreso
@db_session
def put_egreso(egreso_id: int, data: EgresoUpdate) -> dict:
    """Actualiza un egreso"""
    try:
        egreso = Egreso[egreso_id]

        if not egreso:
            raise HTTPException(status_code=404, detail="Egreso no encontrado")

        # Obtener campos a actualizar
        datos = data.dict(exclude_unset=True)

        if not datos:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")

        # Validación adicional del monto
        if "monto" in datos and datos["monto"] <= 0:
            raise HTTPException(status_code=400, detail="El monto debe ser mayor a 0")

        # Actualizar campos
        for campo, valor in datos.items():
            setattr(egreso, campo, valor)

        commit()

        return {
            "id": egreso.id,
            "monto": egreso.monto,
            "categoria": egreso.categoria,
            "fecha": egreso.fecha,
            "fk_usuarios": egreso.fk_usuarios.id
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en put_egreso: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

# DELETE EGRESO - Permite eliminar un egreso por ID
@db_session
def delete_egreso(egreso_id: int):
    """
    Elimina un egreso de la base de datos
    """
    try:
        egreso = Egreso.get(id=egreso_id)

        if not egreso:
            raise HTTPException(status_code=404, detail="Egreso no encontrado")

        egreso.delete()
        
        commit()

        return {"mensaje": f"Egreso con ID {egreso_id} eliminado correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        print("❌ Error en delete_egreso:", e)
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar el egreso: {str(e)}"
        )