# app/services/pasivoService.py
# Contiene la lógica CRUD y las validaciones de negocio antes de interactuar con la base de datos
from typing import List
from pony.orm import db_session, commit
from datetime import date
from app.models.pasivo import Pasivo
from app.models.usuario import Usuario
from app.schemas.pasivo import PasivoCreate, PasivoUpdate


# GET PASIVOS - Devuelve la lista de pasivos
@db_session
def get_pasivos_service(usuario_id: int) -> List[dict]:

    """ Obtiene todos los pasivos del usuario """
    
    try:

        # Traer todos y filtrar manualmente ya que parece haber un bug, esto no da problema en BD pequeñas porque no lo hace lento por los pocos registros
        todos_pasivos = list(Pasivo.select().order_by(Pasivo.id))
        pasivos = [p for p in todos_pasivos if p.fk_usuarios.id == usuario_id]

        resultado = []
        for pasivo in pasivos:
            resultado.append(
                {
                    "id": pasivo.id,
                    "nombre": pasivo.nombre,
                    "tipo": pasivo.tipo,
                    "monto_total": pasivo.monto_total,
                    "pago_mensual": pasivo.pago_mensual,
                    "fecha_vencimiento": pasivo.fecha_vencimiento,
                    "fk_usuarios": pasivo.fk_usuarios.id  # Extraer el ID del usuario
                }
            )

        return resultado

    except Exception as e:
        print(f"❌ Error en get_pasivos_service: {e}")
        raise ValueError(str(e))


# GET PASIVO - Obtener un pasivo por ID
@db_session
def get_pasivo_service(pasivo_id: int) -> dict:
    
    """ Obtiene un pasivo específico por su ID """
    
    try:
        pasivo = Pasivo.get(id=pasivo_id)  

        if not pasivo:
            raise ValueError("Pasivo no encontrado")

        return {
                    "id": pasivo.id,
                    "nombre": pasivo.nombre,
                    "tipo": pasivo.tipo,
                    "monto_total": pasivo.monto_total,
                    "pago_mensual": pasivo.pago_mensual,
                    "fecha_vencimiento": pasivo.fecha_vencimiento,
                    "fk_usuarios": pasivo.fk_usuarios.id  # Extraer el ID del usuario
        }
    except ValueError:
        raise
    except Exception as e:
        print("❌ Error en get_pasivo_service:", e)
        raise ValueError(f"Error al obtener el pasivo: {str(e)}")


# POST PASIVO - Permite crear un pasivo
@db_session
def post_pasivo_service(pasivo_data: PasivoCreate, usuario_id: int):

    """ Crea un nuevo pasivo en la base de datos """

    try:
        # 1. Validar monto total positivo
        if pasivo_data.monto_total <= 0:
            raise ValueError("El monto total debe ser mayor a 0")
        
        # 2. Validar pago mensual positivo
        if pasivo_data.pago_mensual < 0:
            raise ValueError("El pago mensual debe ser mayor o igual a 0")
        
        # 3. Validar fecha de vencimiento no sea en el pasado
        if pasivo_data.fecha_vencimiento < date.today():
            raise ValueError("La fecha de vencimiento no puede ser en el pasado")
        
        # 4. Validar tipo de pasivo
        tipos_validos = {"deuda", "tarjeta", "préstamo", "hipoteca"}
        if pasivo_data.tipo.lower() not in tipos_validos:
            raise ValueError("Tipo de pasivo inválido. Tipos válidos: deuda, tarjeta, prestamo, hipoteca.")

        # Obtener el usuario
        usuario = Usuario.get(id=usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")

        # Crear el nuevo pasivo
        nuevo_pasivo = Pasivo(
            monto_total=pasivo_data.monto_total,
            nombre=pasivo_data.nombre,
            tipo=pasivo_data.tipo,
            pago_mensual=pasivo_data.pago_mensual,
            fecha_vencimiento=pasivo_data.fecha_vencimiento,
            fk_usuarios=usuario,  # Pasar el objeto usuario, no un ID
        )

        commit()

        return {
            "id": nuevo_pasivo.id,
            "monto_total":nuevo_pasivo.monto_total,
            "nombre":nuevo_pasivo.nombre,
            "tipo":nuevo_pasivo.tipo,
            "pago_mensual":nuevo_pasivo.pago_mensual,
            "fecha_vencimiento":nuevo_pasivo.fecha_vencimiento,
            "fk_usuarios": nuevo_pasivo.fk_usuarios.id,
        }

    except ValueError:
        raise
    except Exception as e:
        print("❌ Error en post_pasivo_service:", e)
        raise ValueError(f"Error al crear el pasivo: {str(e)}")


# PUT PASIVO - Permite modificar un pasivo
@db_session
def put_pasivo_service(pasivo_id: int, pasivo_data: PasivoUpdate, usuario_id) -> dict:

    """ Actualiza un pasivo """

    try:
        pasivo = Pasivo.get(id=pasivo_id)
        if not pasivo:
            raise ValueError("Pasivo no encontrado")

        # 1. Validar que le pertenece al usuario
        if pasivo.fk_usuarios.id != usuario_id:
            raise ValueError("No tienes permiso para modificar este pasivo")

        # Obtener campos a actualizar
        datos = pasivo_data.dict(exclude_unset=True)
        if not datos:
            raise ValueError("No hay campos para actualizar")

        # 2. Validar monto total
        if "monto_total" in datos and datos["monto_total"] <= 0:
            raise ValueError("El monto total debe ser mayor a 0")
        
        # 3. Validar pago mensual
        if "pago_mensual" in datos and datos["pago_mensual"] < 0:
            raise ValueError("El pago mensual debe ser mayor o igual 0")
        
        # 4. Validar fecha_vencimiento si se actualiza
        if "fecha_vencimiento" in datos:
            if datos["fecha_vencimiento"] < date.today():
                raise ValueError("La fecha de vencimiento no puede ser en el pasado")
            
        # 5. Validar tipo de pasivo
        tipos_validos = {"deuda", "tarjeta", "prestamo", "hipoteca"}
        if pasivo_data.tipo.lower() not in tipos_validos:
            raise ValueError("Tipo de pasivo inválido. Tipos válidos: deuda, tarjeta, prestamo, hipoteca.")
        
        # Actualizar campos
        for campo, valor in datos.items():
            setattr(pasivo, campo, valor)

        commit()

        return {
                    "id": pasivo.id,
                    "nombre": pasivo.nombre,
                    "tipo": pasivo.tipo,
                    "monto_total": pasivo.monto_total,
                    "pago_mensual": pasivo.pago_mensual,
                    "fecha_vencimiento": pasivo.fecha_vencimiento,
                    "fk_usuarios": pasivo.fk_usuarios.id,
        }

    except ValueError:
        raise
    except Exception as e:
        print(f"❌ Error en put_pasivo_service: {e}")
        raise ValueError(str(e))


# DELETE PASIVO - Permite eliminar un pasivo por ID
@db_session
def delete_pasivo_service(pasivo_id: int, usuario_id: int):

    """ Elimina un pasivo de la base de datos """

    try:
        pasivo = Pasivo.get(id=pasivo_id)

        if not pasivo:
            raise ValueError("Pasivo no encontrado")
        
        # Validar que le pertenece al usuario
        if pasivo.fk_usuarios.id != usuario_id:
            raise ValueError("No tienes permiso para eliminar este pasivo")

        pasivo.delete()

        commit()

        return {"mensaje": f"Pasivo con ID {pasivo_id} eliminado correctamente"}

    except ValueError:
        raise
    except Exception as e:
        print("❌ Error en delete_pasivo_service:", e)
        raise ValueError(f"Error al eliminar el pasivo: {str(e)}")
