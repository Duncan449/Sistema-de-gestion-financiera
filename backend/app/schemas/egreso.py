# app/schemas/egreso.py
from pydantic import BaseModel
from typing import Optional
from datetime import date


class EgresoCreate(BaseModel):
    monto: float
    categoria: str
    fecha: date
    # fk_usuarios: int  # Se elimina este campo ya que se tomará del token


class EgresoUpdate(BaseModel):
    monto: Optional[float] = None
    categoria: Optional[str] = None
    fecha: Optional[date] = None


class EgresoOut(BaseModel):
    id: int
    monto: float
    categoria: str
    fecha: date
    fk_usuarios: int
