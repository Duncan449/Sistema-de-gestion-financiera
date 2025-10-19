# app/routes/egresoRoutes.py
from fastapi import APIRouter, Depends
from typing import List
from app.controllers.egresoControllers import (
    get_egresos_controller,
    get_egreso_controller,
    post_egreso_controller,
    put_egreso_controller,
    delete_egreso_controller,
)
from app.services.auth_service import obtener_usuario_autenticado
from app.schemas.egreso import EgresoCreate, EgresoUpdate, EgresoOut


router = APIRouter(prefix="/egresos", tags=["Egresos"])


@router.get("/", response_model=List[EgresoOut])
def listar_egresos(usuario: dict = Depends(obtener_usuario_autenticado)):
    return get_egresos_controller(usuario)


@router.get("/{egreso_id}", response_model=EgresoOut)
def obtener_egreso(
    egreso_id: int, usuario: dict = Depends(obtener_usuario_autenticado)
):
    return get_egreso_controller(egreso_id, usuario)


@router.post("/", response_model=EgresoOut, status_code=201)
def crear_egreso(
    egreso: EgresoCreate, usuario: dict = Depends(obtener_usuario_autenticado)
):
    return post_egreso_controller(egreso, usuario)


@router.put("/{egreso_id}", response_model=EgresoOut)
def actualizar_egreso(
    egreso_id: int,
    egreso: EgresoUpdate,
    usuario: dict = Depends(obtener_usuario_autenticado),
):
    return put_egreso_controller(egreso_id, egreso, usuario)


@router.delete("/{egreso_id}")
def eliminar_egreso(
    egreso_id: int, usuario: dict = Depends(obtener_usuario_autenticado)
):
    return delete_egreso_controller(egreso_id, usuario)
