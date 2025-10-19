# app/routes/usuarioRoutes.py
from fastapi import APIRouter, Depends
from typing import List
from app.controllers.usuarioControllers import (
    get_usuarios_controller,
    get_usuario_controller,
    put_usuario_controller,
    delete_usuario_controller,
)
from app.services.auth_service import obtener_usuario_autenticado
from app.schemas.usuario import UsuarioUpdate, UsuarioOut

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=List[UsuarioOut])
def listar_usuarios(usuario_auth: dict = Depends(obtener_usuario_autenticado)):
    return get_usuarios_controller(usuario_auth)


@router.get("/{usuario_id}", response_model=UsuarioOut)
def obtener_usuario(
    usuario_id: int, usuario_auth: dict = Depends(obtener_usuario_autenticado)
):
    return get_usuario_controller(usuario_id, usuario_auth)


@router.put("/{usuario_id}", response_model=UsuarioOut)
def actualizar_usuario(
    usuario_id: int,
    usuario: UsuarioUpdate,
    usuario_auth: dict = Depends(obtener_usuario_autenticado),
):
    return put_usuario_controller(usuario_id, usuario, usuario_auth)


@router.delete("/{usuario_id}")
def eliminar_usuario(
    usuario_id: int, usuario_auth: dict = Depends(obtener_usuario_autenticado)
):
    return delete_usuario_controller(usuario_id, usuario_auth)
