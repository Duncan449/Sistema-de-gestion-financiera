# app/schemas/auth.py
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):  # Para la solicitud del login
    email: EmailStr
    password: str

    class Config:
        example = {"email": "usuario@example.com", "password": "micontraseña123"}


class LoginResponse(BaseModel):  # Para la respuesta de login exitoso
    access_token: str
    token_type: str
    usuario_id: int
    email: str
    nombre_completo: str


class RegisterRequest(BaseModel):  # Para el registro de un nuevo usuario
    nombre_completo: str
    email: EmailStr
    username: str
    password: str

    class Config:
        example = {
            "nombre_completo": "Juan Pérez",
            "email": "juan@example.com",
            "username": "juanperez",
            "password": "micontraseña123",
        }


class TokenData(BaseModel):  # Para los datos del token decodificado
    usuario_id: int
    email: str
