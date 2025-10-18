# app/routes/authRoutes.py
from fastapi import APIRouter, Form
from controllers.authControllers import (
    login_controller,
    registrar_controller,
    cambiar_contraseña_controller,
)
from schemas.auth import LoginRequest, LoginResponse, RegisterRequest

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=LoginResponse)
def login(datos: LoginRequest):
    return login_controller(datos.email, datos.password)


@router.post("/register")  # POST - Usuario
def register(datos: RegisterRequest):
    return registrar_controller(
        nombre_completo=datos.nombre_completo,
        email=datos.email,
        username=datos.username,
        password=datos.password,
    )


'''
@router.post("/login-form")
def login_form(email: str = Form(...), password: str = Form(...)):
    """
    Endpoint de login alternativo que acepta form-data.

    Útil para formularios HTML tradicionales.

    Usar cuando el cliente envía:
    Content-Type: application/x-www-form-urlencoded
    email=usuario@example.com&password=micontraseña123
    """
    return login_usuario(email, password)
'''


@router.post("/cambiar-contraseña")
def cambiar_contraseña(usuario_id: int, contraseña_actual: str, contraseña_nueva: str):
    return cambiar_contraseña_controller(
        usuario_id, contraseña_actual, contraseña_nueva
    )
