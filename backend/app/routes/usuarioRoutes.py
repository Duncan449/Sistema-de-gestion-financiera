# app/routes/usuarioRoutes.py
from fastapi import APIRouter
from typing import List
from controllers.usuarioControllers import (
    get_usuarios,
    get_usuario,
    post_usuario,
    put_usuario,
    delete_usuario,
)
from schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioOut

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=List[UsuarioOut])
def listar_usuarios():
    return get_usuarios()


@router.get("/{usuario_id}", response_model=UsuarioOut)
def obtener_usuario(usuario_id: int):
    return get_usuario(usuario_id)


@router.post("/", response_model=UsuarioOut, status_code=201)
def crear_usuario(usuario: UsuarioCreate):
    return post_usuario(usuario)


@router.put("/{usuario_id}", response_model=UsuarioOut)
def actualizar_usuario(usuario_id: int, usuario: UsuarioUpdate):
    return put_usuario(usuario_id, usuario)


@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    return delete_usuario(usuario_id)
