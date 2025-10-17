# app/controllers/ingresoControllers.py
from typing import List
from fastapi import HTTPException
from pony.orm import db_session, commit, select
from models.ingreso import Ingreso
from schemas.ingreso import IngresoOut, IngresoCreate, IngresoUpdate


# GET INGRESOS - Devuelve la lista de ingresos
@db_session
def get_ingresos() -> List[dict]:
    """Obtiene todos los ingresos"""
    try:
        # Usar query más directa
        ingresos_query = Ingreso.select().order_by(Ingreso.id)

        resultado = []
        for ingreso in ingresos_query:
            resultado.append(
                {
                    "id": ingreso.id,
                    "monto": ingreso.monto,
                    "categoria": ingreso.categoria,
                    "fecha": ingreso.fecha,
                    "fk_usuarios": ingreso.fk_usuarios.id  # Extraer el ID del usuario
                }
            )

        return resultado

    except Exception as e:
        print(f"❌ Error en get_ingresos: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
# GET INGRESO - Obtener un ingreso por ID
@db_session
def get_ingreso(ingreso_id: int) -> dict:
    """
    Obtiene un ingreso específico por su ID
    """
    try:
        ingreso = Ingreso.get(id=ingreso_id)

        if not ingreso:
            raise HTTPException(status_code=404, detail="Ingreso no encontrado")

        return {
                    "id": ingreso.id,
                    "monto": ingreso.monto,
                    "categoria": ingreso.categoria,
                    "fecha": ingreso.fecha,
                    "fk_usuarios": ingreso.fk_usuarios.id  # Extraer el ID del usuario
        }
    except HTTPException:
        raise
    except Exception as e:
        print("❌ Error en get_ingreso:", e)
        raise HTTPException(
            status_code=500, detail=f"Error al obtener el ingreso: {str(e)}"
        )
    
# POST INGRESO - Permite crear un ingreso
@db_session
def post_ingreso(ingreso: IngresoCreate):
    """Crea un nuevo ingreso en la base de datos"""
    try:
        from models.usuario import Usuario
        
        # Validación adicional del monto
        if ingreso.monto <= 0:
            raise HTTPException(status_code=400, detail="El monto debe ser mayor a 0")

        # Obtener el usuario
        usuario = Usuario.get(id=ingreso.fk_usuarios)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Crear el nuevo ingreso
        nuevo_ingreso = Ingreso(
            monto=ingreso.monto,
            categoria=ingreso.categoria,
            fecha=ingreso.fecha,
            fk_usuarios=usuario  # Pasar el objeto usuario, no un ID
        )

        commit()

        return {
            "id": nuevo_ingreso.id,
            "monto": nuevo_ingreso.monto,
            "categoria": nuevo_ingreso.categoria,
            "fecha": nuevo_ingreso.fecha,
            "fk_usuarios": nuevo_ingreso.fk_usuarios.id
        }

    except HTTPException:
        raise
    except Exception as e:
        print("❌ Error en post_ingreso:", e)
        raise HTTPException(
            status_code=400, detail=f"Error al crear el ingreso: {str(e)}"
        )
    
# PUT INGRESO - Permite modificar un ingreso
@db_session
def put_ingreso(ingreso_id: int, data: IngresoUpdate) -> dict:
    """Actualiza un ingreso"""
    try:
        ingreso = Ingreso[ingreso_id]

        if not ingreso:
            raise HTTPException(status_code=404, detail="Ingreso no encontrado")

        # Obtener campos a actualizar
        datos = data.dict(exclude_unset=True)

        if not datos:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")

        # Validación adicional del monto
        if ingreso.monto <= 0:
            raise HTTPException(status_code=400, detail="El monto debe ser mayor a 0")

        # Actualizar campos
        for campo, valor in datos.items():
            setattr(ingreso, campo, valor)

        commit()

        return {
            "id": ingreso.id,
            "monto": ingreso.monto,
            "categoria": ingreso.categoria,
            "fecha": ingreso.fecha,
            "fk_usuarios": ingreso.fk_usuarios.id
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en put_usuario: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
# DELETE INGRESO - Permite eliminar un ingreso por ID
@db_session
def delete_ingreso(ingreso_id: int):
    """
    Elimina un ingreso de la base de datos
    """
    try:
        ingreso = Ingreso.get(id=ingreso_id)

        if not ingreso:
            raise HTTPException(status_code=404, detail="Ingreso no encontrado")

        ingreso.delete()
        
        commit()

        return {"mensaje": f"Ingreso con ID {ingreso_id} eliminado correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        print("❌ Error en delete_ingreso:", e)
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar el ingreso: {str(e)}"
        )