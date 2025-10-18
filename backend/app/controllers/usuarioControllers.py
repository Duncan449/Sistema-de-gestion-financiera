# app/controllers/usuarioControllers.py
from typing import List
from fastapi import HTTPException
from pony.orm import db_session, commit, select
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioOut, UsuarioCreate, UsuarioUpdate


# GET USUARIOS - Devuelve la lista de usuarios
@db_session
def get_usuarios() -> List[dict]:
    """Obtiene todos los usuarios"""
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
        print(f"❌ Error en get_usuarios: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# GET USUARIO - Obtener un usuario por ID
@db_session
def get_usuario(usuario_id: int) -> dict:
    """
    Obtiene un usuario específico por su ID
    """
    try:
        usuario = Usuario.get(id=usuario_id)

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return {
            "id": usuario.id,
            "nombre_completo": usuario.nombre_completo,
            "password": usuario.password,
            "email": usuario.email,
            "username": usuario.username,
        }
    except HTTPException:
        raise
    except Exception as e:
        print("❌ Error en get_usuario:", e)
        raise HTTPException(
            status_code=500, detail=f"Error al obtener el usuario: {str(e)}"
        )


# POST USUARIO - Permite crear un usuario
@db_session
def post_usuario(usuario: UsuarioCreate):
    """
    Crea un nuevo usuario en la base de datos
    """
    try:
        # Verificar si ya existe un usuario con ese email o username
        if Usuario.exists(email=usuario.email):
            raise HTTPException(status_code=400, detail="El email ya está registrado")

        if Usuario.exists(username=usuario.username):
            raise HTTPException(
                status_code=400, detail="El username ya está registrado"
            )

        # Crear el nuevo usuario
        nuevo_usuario = Usuario(
            nombre_completo=usuario.nombre_completo,
            password=usuario.password,
            email=usuario.email,
            username=usuario.username,
        )

        commit()  # Guardar los cambios

        return {
            "id": nuevo_usuario.id,
            "nombre_completo": nuevo_usuario.nombre_completo,
            "password": nuevo_usuario.password,
            "email": nuevo_usuario.email,
            "username": nuevo_usuario.username,
        }

    except HTTPException:
        raise
    except Exception as e:
        print("❌ Error en post_usuario:", e)
        raise HTTPException(
            status_code=400, detail=f"Error al crear el usuario: {str(e)}"
        )


# PUT USUARIO - Permite modificar un usuario
@db_session
def put_usuario(usuario_id: int, data: UsuarioUpdate) -> dict:
    """Actualiza un usuario"""
    try:
        usuario = Usuario[usuario_id]

        # Obtener campos a actualizar
        datos = data.dict(exclude_unset=True)

        if not datos:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")

        # Verificar duplicados
        if "email" in datos and datos["email"] != usuario.email:
            if Usuario.exists(email=datos["email"]):
                raise HTTPException(
                    status_code=400, detail="El email ya está registrado"
                )

        if "username" in datos and datos["username"] != usuario.username:
            if Usuario.exists(username=datos["username"]):
                raise HTTPException(
                    status_code=400, detail="El username ya está registrado"
                )

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

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en put_usuario: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# DELETE USUARIO - Permite eliminar un usuario por ID
@db_session
def delete_usuario(usuario_id: int):
    """
    Elimina un usuario de la base de datos
    """
    try:
        usuario = Usuario.get(id=usuario_id)

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        usuario.delete()
        commit()

        return {"mensaje": f"Usuario con ID {usuario_id} eliminado correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        print("❌ Error en delete_usuario:", e)
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar el usuario: {str(e)}"
        )
