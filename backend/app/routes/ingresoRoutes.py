# app/routes/ingresoRoutes.py
from fastapi import APIRouter, Depends
from typing import List
from app.controllers.ingresoControllers import (
    get_ingresos_controller,
    get_ingreso_controller,
    post_ingreso_controller,
    put_ingreso_controller,
    delete_ingreso_controller,
)
from app.services.auth_service import obtener_usuario_autenticado
from app.schemas.ingreso import IngresoCreate, IngresoUpdate, IngresoOut


router = APIRouter(prefix="/ingresos", tags=["Ingresos"])


@router.get("/", response_model=List[IngresoOut])
def listar_ingresos(usuario: dict = Depends(obtener_usuario_autenticado)):
    return get_ingresos_controller(usuario)


@router.get("/{ingreso_id}", response_model=IngresoOut)
def obtener_ingreso(
    ingreso_id: int, usuario: dict = Depends(obtener_usuario_autenticado)
):
    return get_ingreso_controller(ingreso_id, usuario)


@router.post("/", response_model=IngresoOut, status_code=201)
def crear_ingreso(
    ingreso: IngresoCreate, usuario: dict = Depends(obtener_usuario_autenticado)
):
    return post_ingreso_controller(ingreso, usuario)


@router.put("/{ingreso_id}", response_model=IngresoOut)
def actualizar_ingreso(
    ingreso_id: int,
    ingreso: IngresoUpdate,
    usuario: dict = Depends(obtener_usuario_autenticado),
):
    return put_ingreso_controller(ingreso_id, ingreso, usuario)


@router.delete("/{ingreso_id}")
def eliminar_ingreso(
    ingreso_id: int, usuario: dict = Depends(obtener_usuario_autenticado)
):
    return delete_ingreso_controller(ingreso_id, usuario)
