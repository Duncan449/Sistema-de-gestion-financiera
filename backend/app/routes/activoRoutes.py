from fastapi import APIRouter, Depends
from typing import List
from app.controllers.activoControllers import (
    get_activos_controller,
    get_activo_controller,
    post_activo_controller,
    put_activo_controller,
    delete_activo_controller,
)
from app.services.auth_service import obtener_usuario_autenticado
from app.schemas.activo import ActivoCreate, ActivoUpdate, ActivoOut

router = APIRouter(prefix="/activos", tags=["Activos"])


@router.get("/", response_model=List[ActivoOut])
def listar_activos(usuario: dict = Depends(obtener_usuario_autenticado)):
    return get_activos_controller(usuario)


@router.get("/{activo_id}", response_model=ActivoOut)
def obtener_activo(
    activo_id: int, usuario: dict = Depends(obtener_usuario_autenticado)
):
    return get_activo_controller(activo_id, usuario)


@router.post("/", response_model=ActivoOut, status_code=201)
def crear_activo(
    activo: ActivoCreate, usuario: dict = Depends(obtener_usuario_autenticado)
):
    return post_activo_controller(activo, usuario)


@router.put("/{activo_id}", response_model=ActivoOut)
def actualizar_activo(
    activo_id: int,
    activo: ActivoUpdate,
    usuario: dict = Depends(obtener_usuario_autenticado),
):
    return put_activo_controller(activo_id, activo, usuario)


@router.delete("/{activo_id}")
def eliminar_activo(
    activo_id: int, usuario: dict = Depends(obtener_usuario_autenticado)
):
    return delete_activo_controller(activo_id, usuario)
