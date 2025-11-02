# app/schemas/ingreso.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


# Modelo para crear ingreso (input)
class IngresoCreate(BaseModel):
    monto: float
    categoria: str
    fecha: date
    # fk_usuarios: int # Se elimina este campo ya que se tomará del token


# Modelo para actualizaciones (input)
class IngresoUpdate(BaseModel):
    monto: Optional[float] = None
    categoria: Optional[str] = None
    fecha: Optional[date] = None


# Modelo para devolver datos (Output)
class IngresoOut(BaseModel):
    id: int
    monto: float
    categoria: str
    fecha: date
    fk_usuarios: int  # devuelve el ID del usuario, no el objeto
