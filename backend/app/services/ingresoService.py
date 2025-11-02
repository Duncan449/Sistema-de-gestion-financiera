# app/services/ingresoService.py
from typing import List
from pony.orm import db_session, commit
from app.models.ingreso import Ingreso
from app.models.usuario import Usuario
from app.schemas.ingreso import IngresoCreate, IngresoUpdate


# GET INGRESOS - Devuelve la lista de ingresos
@db_session
def get_ingresos_service(usuario_id: int) -> List[dict]:
    """Obtiene todos los ingresos del usuario autenticado"""
    try:

        # Traer todos y filtrar manualmente
        todos_ingresos = list(Ingreso.select().order_by(Ingreso.id))
        ingresos = [p for p in todos_ingresos if p.fk_usuarios.id == usuario_id]

        resultado = []
        for ingreso in ingresos:
            resultado.append(
                {
                    "id": ingreso.id,
                    "monto": ingreso.monto,
                    "categoria": ingreso.categoria,
                    "fecha": ingreso.fecha,
                    "fk_usuarios": ingreso.fk_usuarios.id,  # Extraer el ID del usuario
                }
            )

        return resultado

    except Exception as e:
        print(f"❌ Error en get_ingresos_service: {e}")
        raise ValueError(str(e))


# GET INGRESO - Obtener un ingreso por ID
@db_session
def get_ingreso_service(ingreso_id: int) -> dict:
    """
    Obtiene un ingreso específico por su ID
    """
    try:
        ingreso = Ingreso.get(id=ingreso_id)

        if not ingreso:
            raise ValueError("Ingreso no encontrado")

        return {
            "id": ingreso.id,
            "monto": ingreso.monto,
            "categoria": ingreso.categoria,
            "fecha": ingreso.fecha,
            "fk_usuarios": ingreso.fk_usuarios.id,  # Extraer el ID del usuario
        }
    except ValueError:
        raise
    except Exception as e:
        print("❌ Error en get_ingreso_service:", e)
        raise ValueError(f"Error al obtener el ingreso: {str(e)}")


# POST INGRESO - Permite crear un ingreso
@db_session
def post_ingreso_service(ingreso_data: IngresoCreate, usuario_id: int):
    """Crea un nuevo ingreso en la base de datos"""
    try:
        # Validación adicional del monto
        if ingreso_data.monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")

        # Obtener el usuario
        usuario = Usuario.get(id=usuario_id)  # Toma el usuario del token
        if not usuario:
            raise ValueError("Usuario no encontrado")

        # Crear el nuevo ingreso
        nuevo_ingreso = Ingreso(
            monto=ingreso_data.monto,
            categoria=ingreso_data.categoria,
            fecha=ingreso_data.fecha,
            fk_usuarios=usuario,  # Pasar el objeto usuario, no un ID
        )

        commit()

        return {
            "id": nuevo_ingreso.id,
            "monto": nuevo_ingreso.monto,
            "categoria": nuevo_ingreso.categoria,
            "fecha": nuevo_ingreso.fecha,
            "fk_usuarios": nuevo_ingreso.fk_usuarios.id,
        }

    except ValueError:
        raise
    except Exception as e:
        print("❌ Error en post_ingreso_service:", e)
        raise ValueError(f"Error al crear el ingreso: {str(e)}")


# PUT INGRESO - Permite modificar un ingreso
@db_session
def put_ingreso_service(
    ingreso_id: int, ingreso_data: IngresoUpdate, usuario_id: int
) -> dict:
    """Actualiza un ingreso"""
    try:
        ingreso = Ingreso.get(id=ingreso_id)

        if not ingreso:
            raise ValueError("Ingreso no encontrado")

        # Verificar que el ingreso pertenece al usuario autenticado
        if ingreso.fk_usuarios.id != usuario_id:
            raise ValueError("No tienes permiso para modificar este ingreso")

        # Obtener campos a actualizar
        datos = ingreso_data.dict(exclude_unset=True)

        if not datos:
            raise ValueError("No hay campos para actualizar")

        # Validación adicional del monto
        if "monto" in datos and datos["monto"] <= 0:
            raise ValueError("El monto debe ser mayor a 0")

        # Actualizar campos
        for campo, valor in datos.items():
            setattr(ingreso, campo, valor)

        commit()

        return {
            "id": ingreso.id,
            "monto": ingreso.monto,
            "categoria": ingreso.categoria,
            "fecha": ingreso.fecha,
            "fk_usuarios": ingreso.fk_usuarios.id,
        }

    except ValueError:
        raise
    except Exception as e:
        print(f"❌ Error en put_ingreso_service: {e}")
        raise ValueError(str(e))


# DELETE INGRESO - Permite eliminar un ingreso por ID
@db_session
def delete_ingreso_service(ingreso_id: int, usuario_id: int):
    """
    Elimina un ingreso de la base de datos
    """
    try:
        ingreso = Ingreso.get(id=ingreso_id)

        if not ingreso:
            raise ValueError("Ingreso no encontrado")

        # Verificar que el ingreso pertenece al usuario autenticado
        if ingreso.fk_usuarios.id != usuario_id:
            raise ValueError("No tienes permiso para eliminar este ingreso")

        ingreso.delete()

        commit()

        return {"mensaje": f"Ingreso con ID {ingreso_id} eliminado correctamente"}

    except ValueError:
        raise
    except Exception as e:
        print("❌ Error en delete_ingreso_service:", e)
        raise ValueError(f"Error al eliminar el ingreso: {str(e)}")
