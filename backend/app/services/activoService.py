from typing import List
from pony.orm import db_session, commit
from app.models.activo import Activo
from app.models.usuario import Usuario
from app.schemas.activo import ActivoCreate, ActivoUpdate


# GET ACTIVOS - Devuelve la lista de activos
@db_session
def get_activos_service(usuario_id: int) -> List[dict]:
    """Obtiene todos los activos del usuario autenticado"""
    try:

        # Traer todos y filtrar manualmente
        todos_activos = list(Activo.select().order_by(Activo.id))
        activos = [p for p in todos_activos if p.fk_usuarios.id == usuario_id]

        resultado = []
        for activo in activos:
            resultado.append(
                {
                    "id": activo.id,
                    "valor": activo.valor,
                    "tipo": activo.tipo,
                    "nombre": activo.nombre,
                    "flujo_mensual": activo.flujo_mensual,
                    "fk_usuarios": activo.fk_usuarios.id,
                }
            )

        return resultado

    except Exception as e:
        print(f"❌ Error en get_activos_service: {e}")
        raise ValueError(str(e))


# GET ACTIVO - Obtener un activo por ID
@db_session
def get_activo_service(activo_id: int) -> dict:
    """
    Obtiene un activo específico por ID.
    """
    try:
        activo = Activo.get(id=activo_id)

        if not activo:
            raise ValueError(f"Activo con ID {activo_id} no encontrado")

        return {
            "id": activo.id,
            "valor": activo.valor,
            "tipo": activo.tipo,
            "nombre": activo.nombre,
            "flujo_mensual": activo.flujo_mensual,
            "fk_usuarios": activo.fk_usuarios.id,  # Extraer el ID del usuario
        }

    except ValueError:
        raise
    except Exception as e:
        print(f"Error en get_activo_service: {e}")
        raise ValueError(f"Error al obtener activo: {str(e)}")


# POST ACTIVO - Permite crear un activo
@db_session
def post_activo_service(activo_data: ActivoCreate, usuario_id: int):
    """Crea un nuevo activo en la base de datos"""
    try:
        # Validación adicional del valor
        if activo_data.valor <= 0:
            raise ValueError("El valor debe ser mayor a 0")

        if activo_data.flujo_mensual < 0:
            raise ValueError("El flujo mensual no puede ser negativo")

        # Obtener el usuario
        usuario = Usuario.get(id=usuario_id)  # Toma el usuario del token
        if not usuario:
            raise ValueError("Usuario no encontrado")

        # Crear el nuevo activo
        nuevo_activo = Activo(
            valor=activo_data.valor,
            tipo=activo_data.tipo,
            nombre=activo_data.nombre,
            flujo_mensual=activo_data.flujo_mensual,
            fk_usuarios=usuario,
        )

        commit()

        return {
            "id": nuevo_activo.id,
            "valor": nuevo_activo.valor,
            "tipo": nuevo_activo.tipo,
            "nombre": nuevo_activo.nombre,
            "flujo_mensual": nuevo_activo.flujo_mensual,
            "fk_usuarios": nuevo_activo.fk_usuarios.id,
        }

    except ValueError:
        raise
    except Exception as e:
        print("❌ Error en post_activo_service:", e)
        raise ValueError(f"Error al crear el activo: {str(e)}")


# PUT ACTIVO - Permite modificar un activo
@db_session
def put_activo_service(
    activo_id: int, activo_data: ActivoUpdate, usuario_id: int
) -> dict:
    """Actualiza un activo"""
    try:
        activo = Activo.get(id=activo_id)

        if not activo:
            raise ValueError("Activo no encontrado")

        # Validar que el activo pertenece al usuario
        if activo.fk_usuarios.id != usuario_id:
            raise ValueError("No tienes permiso para modificar este activo")

        # Obtener campos a actualizar
        datos = activo_data.dict(exclude_unset=True)

        if not datos:
            raise ValueError("No hay campos para actualizar")

        # Validación adicional del valor
        if "valor" in datos and datos["valor"] <= 0:
            raise ValueError("El valor debe ser mayor a 0")

        if "flujo_mensual" in datos and datos["flujo_mensual"] < 0:
            raise ValueError("El flujo mensual no puede ser negativo")

        # Actualizar campos
        for campo, valor in datos.items():
            setattr(activo, campo, valor)

        commit()

        return {
            "id": activo.id,
            "valor": activo.valor,
            "tipo": activo.tipo,
            "nombre": activo.nombre,
            "flujo_mensual": activo.flujo_mensual,
            "fk_usuarios": activo.fk_usuarios.id,
        }

    except ValueError:
        raise
    except Exception as e:
        print(f"❌ Error en put_activo_service: {e}")
        raise ValueError(str(e))


# DELETE ACTIVO - Permite eliminar un activo por ID
@db_session
def delete_activo_service(activo_id: int, usuario_id: int):
    """
    Elimina un activo de la base de datos
    """
    try:
        activo = Activo.get(id=activo_id)

        if not activo:
            raise ValueError("Activo no encontrado")

        # Validar que el activo pertenece al usuario
        if activo.fk_usuarios.id != usuario_id:
            raise ValueError("No tienes permiso para eliminar este activo")

        activo.delete()

        commit()

        return {"mensaje": f"Activo con ID {activo_id} eliminado correctamente"}

    except ValueError:
        raise
    except Exception as e:
        print(f"❌ Error en delete_activo_service:", e)
        raise ValueError(f"Error al eliminar el activo: {str(e)}")
