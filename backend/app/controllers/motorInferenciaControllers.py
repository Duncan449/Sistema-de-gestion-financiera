# app/controllers/motorInferenciaController.py
from fastapi import HTTPException
from app.services.motorInferenciaService import (
    evaluar_salud_financiera,
    obtener_ingresos_totales_usuario,
    obtener_egresos_totales_usuario,
    obtener_egresos_por_categoria,
)
from app.services.motorInferenciaService import (
    regla_50_30_20,
    regla_limite_endeudamiento,
    regla_gasta_mas_que_gana,
    regla_fondo_emergencia,
    regla_sin_inversiones,
    regla_inversion_educacion,
    regla_lujos_vs_educacion,
    regla_reserva_imprevistos,
    obtener_valor_total_activos,
    obtener_flujo_mensual_activos,
)


def validar_permiso_usuario(usuario_id: int, usuario_autenticado: dict):
    """Valida que el usuario solo pueda ver su propio análisis"""
    if usuario_autenticado["usuario_id"] != usuario_id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para ver el análisis de otro usuario",
        )


def evaluar_salud_financiera_controller(
    usuario_id: int, usuario_autenticado: dict, dias: int = 30
) -> dict:
    """Controller para evaluar todas las reglas"""
    try:
        validar_permiso_usuario(usuario_id, usuario_autenticado)
        resultado = evaluar_salud_financiera(usuario_id, dias)
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en evaluar_salud_financiera_controller: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error al evaluar salud financiera: {str(e)}"
        )


def evaluar_regla_50_30_20_controller(
    usuario_id: int, usuario_autenticado: dict, dias: int = 30
) -> dict:
    """REGLA 1: Distribución 50/30/20"""
    try:
        validar_permiso_usuario(usuario_id, usuario_autenticado)

        ingresos = obtener_ingresos_totales_usuario(usuario_id, dias)

        gastos_necesidades = (
            obtener_egresos_por_categoria(usuario_id, "vivienda", dias)
            + obtener_egresos_por_categoria(usuario_id, "comida", dias)
            + obtener_egresos_por_categoria(usuario_id, "transporte", dias)
            + obtener_egresos_por_categoria(usuario_id, "salud", dias)
            + obtener_egresos_por_categoria(usuario_id, "servicios", dias)
        )

        gastos_deseos = (
            obtener_egresos_por_categoria(usuario_id, "entretenimiento", dias)
            + obtener_egresos_por_categoria(usuario_id, "restaurantes", dias)
            + obtener_egresos_por_categoria(usuario_id, "viajes", dias)
            + obtener_egresos_por_categoria(usuario_id, "lujos", dias)
        )

        gastos_ahorros = obtener_egresos_por_categoria(
            usuario_id, "ahorro", dias
        ) + obtener_egresos_por_categoria(usuario_id, "inversión", dias)

        return regla_50_30_20(
            ingresos, gastos_necesidades, gastos_deseos, gastos_ahorros
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en evaluar_regla_50_30_20_controller: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def evaluar_limite_endeudamiento_controller(
    usuario_id: int, usuario_autenticado: dict, dias: int = 30
) -> dict:
    """REGLA 2: Límite de endeudamiento"""
    try:
        validar_permiso_usuario(usuario_id, usuario_autenticado)

        ingresos = obtener_ingresos_totales_usuario(usuario_id, dias)
        deudas = obtener_egresos_por_categoria(usuario_id, "deudas", dias)

        return regla_limite_endeudamiento(ingresos, deudas)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def evaluar_gasta_mas_que_gana_controller(
    usuario_id: int, usuario_autenticado: dict, dias: int = 30
) -> dict:
    """REGLA 3: Usuario gasta más de lo que gana"""
    try:
        validar_permiso_usuario(usuario_id, usuario_autenticado)

        ingresos = obtener_ingresos_totales_usuario(usuario_id, dias)
        egresos = obtener_egresos_totales_usuario(usuario_id, dias)

        return regla_gasta_mas_que_gana(ingresos, egresos)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def evaluar_fondo_emergencia_controller(
    usuario_id: int, usuario_autenticado: dict, dias: int = 30
) -> dict:
    """REGLA 4: Fondo de emergencia"""
    try:
        validar_permiso_usuario(usuario_id, usuario_autenticado)

        ingresos = obtener_ingresos_totales_usuario(usuario_id, dias)
        ahorro_total = obtener_egresos_por_categoria(usuario_id, "ahorro", dias) * 6

        return regla_fondo_emergencia(ingresos, ahorro_total)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def evaluar_sin_inversiones_controller(
    usuario_id: int, usuario_autenticado: dict, dias: int = 30
) -> dict:
    try:
        validar_permiso_usuario(usuario_id, usuario_autenticado)

        valor_activos = obtener_valor_total_activos(usuario_id)
        flujo_activos = obtener_flujo_mensual_activos(usuario_id)

        return regla_sin_inversiones(valor_activos, flujo_activos)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def evaluar_inversion_educacion_controller(
    usuario_id: int, usuario_autenticado: dict, dias: int = 30
) -> dict:
    """REGLA 6: Inversión en educación"""
    try:
        validar_permiso_usuario(usuario_id, usuario_autenticado)

        ingresos = obtener_ingresos_totales_usuario(usuario_id, dias)
        educacion = obtener_egresos_por_categoria(usuario_id, "educación", dias)

        return regla_inversion_educacion(educacion, ingresos)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def evaluar_lujos_vs_educacion_controller(
    usuario_id: int, usuario_autenticado: dict, dias: int = 30
) -> dict:
    """REGLA 7: Lujos vs educación/activos"""
    try:
        validar_permiso_usuario(usuario_id, usuario_autenticado)

        lujos = obtener_egresos_por_categoria(usuario_id, "lujos", dias)
        educacion = obtener_egresos_por_categoria(usuario_id, "educación", dias)
        activos = obtener_egresos_por_categoria(usuario_id, "activos", dias)

        return regla_lujos_vs_educacion(lujos, educacion, activos)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def evaluar_reserva_imprevistos_controller(
    usuario_id: int, usuario_autenticado: dict, dias: int = 30
) -> dict:
    """REGLA 8: Reserva para imprevistos"""
    try:
        validar_permiso_usuario(usuario_id, usuario_autenticado)

        ingresos = obtener_ingresos_totales_usuario(usuario_id, dias)
        ahorro_liquido = obtener_egresos_por_categoria(usuario_id, "ahorro", dias)

        return regla_reserva_imprevistos(ingresos, ahorro_liquido)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
