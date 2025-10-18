# app/routes/egresoRoutes.py
from fastapi import APIRouter, Depends
from typing import List
from app.controllers.egresoControllers import (
    get_egresos,
    get_egreso,
    post_egreso,
    put_egreso,
    delete_egreso
)
from app.schemas.egreso import EgresoCreate, EgresoUpdate, EgresoOut


# Función que retorna el usuario_id automáticamente
def get_usuario_id() -> int:
    return 4  # Por ahora retorna 1 para testing


router = APIRouter(prefix="/egresos", tags=["Egresos"])


@router.get("/", response_model=List[EgresoOut])
def listar_egresos():
    return get_egresos()


@router.get("/{egreso_id}", response_model=EgresoOut)
def obtener_egreso(egreso_id: int):
    return get_egreso(egreso_id)


@router.post("/", response_model=EgresoOut, status_code=201)
def crear_egreso(
    egreso: EgresoCreate):
    return post_egreso(egreso)


@router.put("/{egreso_id}", response_model=EgresoOut)
def actualizar_egreso(egreso_id: int, egreso: EgresoUpdate):
    return put_egreso(egreso_id, egreso)


@router.delete("/{egreso_id}")
def eliminar_egreso(egreso_id: int):
    return delete_egreso(egreso_id)