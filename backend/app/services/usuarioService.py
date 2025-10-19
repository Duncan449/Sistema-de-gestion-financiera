# app/services/usuarioService.py
from pony.orm import db_session, commit
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioUpdate


# IMPORTANTE: En services NO hay HTTPException ni respuestas HTTP
# Solo devolvemos datos o lanzamos excepciones de Python


# GET USUARIOS - Devuelve la lista de usuarios
@db_session
def get_usuarios() -> list:
    """
    Obtiene todos los usuarios de la BD.
    """
    try:
        # Usar query más directa
        usuarios_query = Usuario.select().order_by(Usuario.id)

        resultado = []
        for usuario in usuarios_query:
            resultado.append(
                {
                    "id": usuario.id,
                    "nombre_completo": usuario.nombre_completo,
                    "password": usuario.password,
                    "email": usuario.email,
                    "username": usuario.username,
                }
            )

        return resultado

    except Exception as e:
        print(f"Error en get_usuarios: {e}")
        raise ValueError(f"Error al obtener usuarios: {str(e)}")


# GET USUARIO - Obtener un usuario por ID
@db_session
def get_usuario(usuario_id: int) -> dict:
    """
    Obtiene un usuario específico por ID.
    """
    try:
        usuario = Usuario.get(id=usuario_id)

        if not usuario:
            raise ValueError(f"Usuario con ID {usuario_id} no encontrado")

        return {
            "id": usuario.id,
            "nombre_completo": usuario.nombre_completo,
            "password": usuario.password,
            "email": usuario.email,
            "username": usuario.username,
        }

    except ValueError:
        raise
    except Exception as e:
        print(f"Error en get_usuario: {e}")
        raise ValueError(f"Error al obtener usuario: {str(e)}")


# PUT USUARIO - Permite modificar un usuario
@db_session
def put_usuario(usuario_id: int, data: UsuarioUpdate) -> dict:
    """
    Actualiza un usuario existente.
    """
    try:
        usuario = Usuario.get(id=usuario_id)

        if not usuario:
            raise ValueError(f"Usuario con ID {usuario_id} no encontrado")

        # Obtener campos a actualizar
        datos = data.dict(exclude_unset=True)

        if not datos:
            raise ValueError("No hay campos para actualizar")

        # IMPORTANTE: No permitir cambiar contraseña desde aquí
        if "password" in datos:
            raise ValueError(
                "No puedes cambiar la contraseña aquí. Usa POST /auth/cambiar-contraseña"
            )

        # Verificar duplicados de email
        if "email" in datos and datos["email"] != usuario.email:
            if Usuario.get(email=datos["email"]):
                raise ValueError("El email ya está registrado")

        # Verificar duplicados de username
        if "username" in datos and datos["username"] != usuario.username:
            if Usuario.get(username=datos["username"]):
                raise ValueError("El username ya está registrado")

        # Actualizar campos
        for campo, valor in datos.items():
            setattr(usuario, campo, valor)

        commit()

        return {
            "id": usuario.id,
            "nombre_completo": usuario.nombre_completo,
            "password": usuario.password,
            "email": usuario.email,
            "username": usuario.username,
        }

    except ValueError:
        raise
    except Exception as e:
        print(f"Error en put_usuario: {e}")
        raise ValueError(f"Error al actualizar usuario: {str(e)}")


# DELETE USUARIO - Permite eliminar un usuario por ID
@db_session
def delete_usuario(usuario_id: int) -> dict:
    """
    Elimina un usuario de la BD.
    """
    try:
        usuario = Usuario.get(id=usuario_id)

        if not usuario:
            raise ValueError(f"Usuario con ID {usuario_id} no encontrado")

        usuario.delete()
        commit()

        return {"mensaje": f"Usuario con ID {usuario_id} eliminado correctamente"}

    except ValueError:
        raise
    except Exception as e:
        print(f"Error en delete_usuario: {e}")
        raise ValueError(f"Error al eliminar usuario: {str(e)}")
