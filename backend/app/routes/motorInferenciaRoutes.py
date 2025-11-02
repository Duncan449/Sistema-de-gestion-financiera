# app/routes/motorInferenciaRoutes.py
from fastapi import APIRouter, Depends, Query
from app.controllers.motorInferenciaControllers import (
    evaluar_salud_financiera_controller,
    evaluar_regla_50_30_20_controller,
    evaluar_limite_endeudamiento_controller,
    evaluar_gasta_mas_que_gana_controller,
    evaluar_fondo_emergencia_controller,
    evaluar_sin_inversiones_controller,
    evaluar_inversion_educacion_controller,
    evaluar_lujos_vs_educacion_controller,
    evaluar_reserva_imprevistos_controller,
)
from app.services.auth_service import obtener_usuario_autenticado


router = APIRouter(prefix="/analisis", tags=["Motor de Inferencia"])


@router.get("/salud-financiera/{usuario_id}")
def obtener_salud_financiera(
    usuario_id: int,
    usuario: dict = Depends(obtener_usuario_autenticado),
    dias: int = Query(30, description="Período de análisis en días", ge=1, le=365),
):
    """
    Evalúa la salud financiera completa de un usuario (todas las reglas).
    """
    return evaluar_salud_financiera_controller(usuario_id, usuario, dias)


@router.get("/50-30-20/{usuario_id}")
def evaluar_regla_50_30_20(
    usuario_id: int,
    usuario: dict = Depends(obtener_usuario_autenticado),
    dias: int = Query(30, ge=1, le=365),
):
    """
    REGLA 1: Distribución 50/30/20

    Evalúa si los gastos cumplen la regla:
    - 50% necesidades (vivienda, comida, servicios)
    - 30% deseos (entretenimiento, lujos)
    - 20% ahorro/inversión
    """
    return evaluar_regla_50_30_20_controller(usuario_id, usuario, dias)


@router.get("/limite-endeudamiento/{usuario_id}")
def evaluar_limite_endeudamiento(
    usuario_id: int,
    usuario: dict = Depends(obtener_usuario_autenticado),
    dias: int = Query(30, ge=1, le=365),
):
    """
    REGLA 2: Límite de endeudamiento

    Las deudas no deben superar el 40% de los ingresos mensuales.
    """
    return evaluar_limite_endeudamiento_controller(usuario_id, usuario, dias)


@router.get("/deficit-financiero/{usuario_id}")
def evaluar_deficit_financiero(
    usuario_id: int,
    usuario: dict = Depends(obtener_usuario_autenticado),
    dias: int = Query(30, ge=1, le=365),
):
    """
    REGLA 3: Usuario gasta más de lo que gana

    Detecta si hay déficit financiero (egresos > ingresos).
    """
    return evaluar_gasta_mas_que_gana_controller(usuario_id, usuario, dias)


@router.get("/fondo-emergencia/{usuario_id}")
def evaluar_fondo_emergencia(
    usuario_id: int,
    usuario: dict = Depends(obtener_usuario_autenticado),
    dias: int = Query(30, ge=1, le=365),
):
    """
    REGLA 4: Fondo de emergencia

    Debes tener ahorrado entre 3 y 6 meses de gastos fijos.
    """
    return evaluar_fondo_emergencia_controller(usuario_id, usuario, dias)


@router.get("/sin-inversiones/{usuario_id}")
def evaluar_sin_inversiones(
    usuario_id: int,
    usuario: dict = Depends(obtener_usuario_autenticado),
    dias: int = Query(30, ge=1, le=365),
):
    """
    REGLA 5: Usuario no registra inversiones ni activos

    Detecta si el usuario no está invirtiendo en su futuro.
    """
    return evaluar_sin_inversiones_controller(usuario_id, usuario, dias)


@router.get("/inversion-educacion/{usuario_id}")
def evaluar_inversion_educacion(
    usuario_id: int,
    usuario: dict = Depends(obtener_usuario_autenticado),
    dias: int = Query(30, ge=1, le=365),
):
    """
    REGLA 6: Inversión en educación

    Se recomienda invertir al menos 5% de ingresos en educación.
    """
    return evaluar_inversion_educacion_controller(usuario_id, usuario, dias)


@router.get("/lujos-vs-educacion/{usuario_id}")
def evaluar_lujos_vs_educacion(
    usuario_id: int,
    usuario: dict = Depends(obtener_usuario_autenticado),
    dias: int = Query(30, ge=1, le=365),
):
    """
    REGLA 7: Usuario invierte más en lujos que en educación/activos

    Detecta prioridades financieras desbalanceadas.
    """
    return evaluar_lujos_vs_educacion_controller(usuario_id, usuario, dias)


@router.get("/reserva-imprevistos/{usuario_id}")
def evaluar_reserva_imprevistos(
    usuario_id: int,
    usuario: dict = Depends(obtener_usuario_autenticado),
    dias: int = Query(30, ge=1, le=365),
):
    """
    REGLA 8: Reserva para imprevistos menores

    Debes tener al menos 1 mes de ingresos en ahorro líquido.
    """
    return evaluar_reserva_imprevistos_controller(usuario_id, usuario, dias)
