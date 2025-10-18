# app/routes/usuarioRoutes.py
from fastapi import APIRouter
from typing import List
from controllers.usuarioControllers import (
    get_usuarios_controller,
    get_usuario_controller,
    put_usuario_controller,
    delete_usuario_controller,
)
from schemas.usuario import UsuarioUpdate, UsuarioOut

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=List[UsuarioOut])
def listar_usuarios():
    return get_usuarios_controller()


@router.get("/{usuario_id}", response_model=UsuarioOut)
def obtener_usuario(usuario_id: int):
    return get_usuario_controller(usuario_id)


@router.put("/{usuario_id}", response_model=UsuarioOut)
def actualizar_usuario(usuario_id: int, usuario: UsuarioUpdate):
    return put_usuario_controller(usuario_id, usuario)


@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    return delete_usuario_controller(usuario_id)
