# app/schemas/activo.py
from pydantic import BaseModel
from typing import Literal, Optional
from datetime import date


# Modelo para crear activo (input)
class ActivoCreate(BaseModel):
    tipo: Literal[
        "Inmueble", "Vehiculo", "Inversión", "Ahorro", "Negocio", "Otro"
    ]  # Opciones válidas
    valor: float
    nombre: str
    flujo_mensual: Optional[float] = None
    # fk_usuarios: int # Se elimina este campo ya que se tomará del token


# Modelo para actualizaciones (input)
class ActivoUpdate(BaseModel):
    tipo: Optional[str] = None
    valor: Optional[float] = None
    nombre: Optional[str] = None
    flujo_mensual: Optional[float] = None


# Modelo para devolver datos (Output)
class ActivoOut(BaseModel):
    id: int
    tipo: str
    valor: float
    nombre: str
    flujo_mensual: Optional[float] = None
    fk_usuarios: int  # devuelve el ID del usuario, no el objeto
