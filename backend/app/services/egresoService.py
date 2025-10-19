# app/services/egresoService.py
from typing import List
from pony.orm import db_session, commit
from app.models.egreso import Egreso
from app.models.usuario import Usuario
from app.schemas.egreso import EgresoCreate, EgresoUpdate


# GET EGRESOS - Devuelve la lista de egresos
@db_session
def get_egresos_service() -> List[dict]:
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
                    "fk_usuarios": egreso.fk_usuarios.id,  # Extraer el ID del usuario
                }
            )

        return resultado

    except Exception as e:
        print(f"❌ Error en get_egresos_service: {e}")
        raise ValueError(str(e))


# GET EGRESO - Obtener un egreso por ID
@db_session
def get_egreso_service(egreso_id: int) -> dict:
    """
    Obtiene un egreso específico por su ID
    """
    try:
        egreso = Egreso.get(id=egreso_id)

        if not egreso:
            raise ValueError("Egreso no encontrado")

        return {
            "id": egreso.id,
            "monto": egreso.monto,
            "categoria": egreso.categoria,
            "fecha": egreso.fecha,
            "fk_usuarios": egreso.fk_usuarios.id,  # Extraer el ID del usuario
        }
    except ValueError:
        raise
    except Exception as e:
        print("❌ Error en get_egreso_service:", e)
        raise ValueError(f"Error al obtener el egreso: {str(e)}")


# POST EGRESO - Permite crear un egreso
@db_session
def post_egreso_service(egreso_data: EgresoCreate):
    """Crea un nuevo egreso en la base de datos"""
    try:
        # Validación adicional del monto
        if egreso_data.monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")

        # Obtener el usuario
        usuario = Usuario.get(id=egreso_data.fk_usuarios)
        if not usuario:
            raise ValueError("Usuario no encontrado")

        # Crear el nuevo egreso
        nuevo_egreso = Egreso(
            monto=egreso_data.monto,
            categoria=egreso_data.categoria,
            fecha=egreso_data.fecha,
            fk_usuarios=usuario,  # Pasar el objeto usuario, no un ID
        )

        commit()

        return {
            "id": nuevo_egreso.id,
            "monto": nuevo_egreso.monto,
            "categoria": nuevo_egreso.categoria,
            "fecha": nuevo_egreso.fecha,
            "fk_usuarios": nuevo_egreso.fk_usuarios.id,
        }

    except ValueError:
        raise
    except Exception as e:
        print("❌ Error en post_egreso_service:", e)
        raise ValueError(f"Error al crear el egreso: {str(e)}")


# PUT EGRESO - Permite modificar un egreso
@db_session
def put_egreso_service(egreso_id: int, data: EgresoUpdate) -> dict:
    """Actualiza un egreso"""
    try:
        egreso = Egreso.get(id=egreso_id)

        if not egreso:
            raise ValueError("Egreso no encontrado")

        # Obtener campos a actualizar
        datos = data.dict(exclude_unset=True)

        if not datos:
            raise ValueError("No hay campos para actualizar")

        # Validación adicional del monto
        if "monto" in datos and datos["monto"] <= 0:
            raise ValueError("El monto debe ser mayor a 0")

        # Actualizar campos
        for campo, valor in datos.items():
            setattr(egreso, campo, valor)

        commit()

        return {
            "id": egreso.id,
            "monto": egreso.monto,
            "categoria": egreso.categoria,
            "fecha": egreso.fecha,
            "fk_usuarios": egreso.fk_usuarios.id,
        }

    except ValueError:
        raise
    except Exception as e:
        print(f"❌ Error en put_egreso_service: {e}")
        raise ValueError(str(e))


# DELETE EGRESO - Permite eliminar un egreso por ID
@db_session
def delete_egreso_service(egreso_id: int):
    """
    Elimina un egreso de la base de datos
    """
    try:
        egreso = Egreso.get(id=egreso_id)

        if not egreso:
            raise ValueError("Egreso no encontrado")

        egreso.delete()

        commit()

        return {"mensaje": f"Egreso con ID {egreso_id} eliminado correctamente"}

    except ValueError:
        raise
    except Exception as e:
        print("❌ Error en delete_egreso_service:", e)
        raise ValueError(f"Error al eliminar el egreso: {str(e)}")
