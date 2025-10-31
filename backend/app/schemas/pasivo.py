# app/schemas/pasivo.py
# Schemas de Pydantic para validación de datos de entrada/salida
from pydantic import BaseModel
from typing import Optional
from datetime import date

# Modelo para crear pasivo (input)
class PasivoCreate(BaseModel):
    """
    Schema para crear un nuevo pasivo
    Define los campos obligatorios que debe enviar el cliente
    No incluye 'id' (se genera automáticamente) ni 'fk_usuarios' (viene del JWT)

    """
    nombre: str
    tipo: str
    monto_total: float
    pago_mensual: float
    fecha_vencimiento: date

# Modelo para actualizaciones (input)
class PasivoUpdate(BaseModel):
    """
    Schema para actualizar un pasivo existente
    Todos los campos son opcionales para permitir actualizaciones parciales
    Solo se actualizan los campos que se envíen

    """
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    monto_total: Optional[float] = None
    pago_mensual: Optional[float] = None
    fecha_vencimiento: Optional[date] = None

# Modelo para devolver datos (Output)
class PasivoOut(BaseModel):
    """
    Schema para devolver datos de un pasivo
    Define la estructura de la respuesta JSON
    Incluye todos los campos incluyendo 'id' y 'fk_usuarios'
    
    """
    id: int
    nombre: str
    tipo: str
    monto_total: float
    pago_mensual: float
    fecha_vencimiento: date
    fk_usuarios: int