# app/routes/pasivoRoutes.py
# Define los endpoints HTTP para operaciones CRUD de pasivos
from fastapi import APIRouter, Depends
from typing import List
from app.controllers.pasivoControllers import (
    get_pasivos_controller,
    get_pasivo_controller,
    post_pasivo_controller,
    put_pasivo_controller,
    delete_pasivo_controller,
)
from app.services.auth_service import obtener_usuario_autenticado
from app.schemas.pasivo import PasivoCreate, PasivoUpdate, PasivoOut


router = APIRouter(prefix="/pasivos", tags=["Pasivos"])


@router.get("/", response_model=List[PasivoOut])
def listar_pasivos(usuario: dict = Depends(obtener_usuario_autenticado)):
    return get_pasivos_controller(usuario)


@router.get("/{pasivo_id}", response_model=PasivoOut)
def obtener_pasivo(
    pasivo_id: int, usuario: dict = Depends(obtener_usuario_autenticado)
):
    return get_pasivo_controller(pasivo_id, usuario)


@router.post("/", response_model=PasivoOut, status_code=201)
def crear_pasivo(
    pasivo: PasivoCreate, usuario: dict = Depends(obtener_usuario_autenticado)
):
    return post_pasivo_controller(pasivo, usuario)


@router.put("/{pasivo_id}", response_model=PasivoOut)
def actualizar_pasivo(
    pasivo_id: int,
    pasivo: PasivoUpdate,
    usuario: dict = Depends(obtener_usuario_autenticado),
):
    return put_pasivo_controller(pasivo_id, pasivo, usuario)


@router.delete("/{pasivo_id}")
def eliminar_pasivo(
    pasivo_id: int, usuario: dict = Depends(obtener_usuario_autenticado)
):
    return delete_pasivo_controller(pasivo_id, usuario)
