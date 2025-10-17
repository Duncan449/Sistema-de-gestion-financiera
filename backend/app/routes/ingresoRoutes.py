# app/routes/ingresoRoutes.py
from fastapi import APIRouter, Depends
from typing import List
from controllers.ingresoControllers import (
    get_ingresos,
    get_ingreso,
    post_ingreso,
    put_ingreso,
    delete_ingreso
)
from schemas.ingreso import IngresoCreate, IngresoUpdate, IngresoOut

# Función que retorna el usuario_id automáticamente
def get_usuario_id() -> int:
    return 4  # Por ahora retorna 1 para testing

router = APIRouter(prefix="/ingresos", tags=["Ingresos"])

@router.get("/", response_model=List[IngresoOut])
def listar_ingresos():
    return get_ingresos()

@router.get("/{ingreso_id}", response_model=IngresoOut)
def obtener_ingreso(ingreso_id: int):
    return get_ingreso(ingreso_id)

@router.post("/", response_model=IngresoOut, status_code=201)
def crear_ingreso(
    ingreso: IngresoCreate):
     return post_ingreso(ingreso)

@router.put("/{ingreso_id}", response_model=IngresoOut)
def actualizar_ingreso(ingreso_id: int, ingreso: IngresoUpdate):
    return put_ingreso(ingreso_id, ingreso)

@router.delete("/{ingreso_id}")
def eliminar_ingreso(ingreso_id: int):
    return delete_ingreso(ingreso_id)
     