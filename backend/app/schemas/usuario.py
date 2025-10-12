# app/schemas/usuario.py
from pydantic import BaseModel, EmailStr
from typing import Optional


# Modelo para crear usuario (input)
class UsuarioCreate(BaseModel):
    nombre_completo: str
    password: str
    email: EmailStr
    username: str


# Modelo para actualizaciones (input)
class UsuarioUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None


# Modelo para devolver datos (Output)
class UsuarioOut(BaseModel):
    id: int
    nombre_completo: str
    password: str
    email: str
    username: str
