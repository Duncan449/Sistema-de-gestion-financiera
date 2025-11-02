# app/services/motorInferenciaService.py
from typing import List, Dict
from pony.orm import db_session
from app.models.ingreso import Ingreso
from app.models.egreso import Egreso
from app.models.activo import Activo
from app.models.pasivo import Pasivo
from datetime import datetime, timedelta

# ============================================================
# FUNCIONES AUXILIARES (con filtrado manual para evitar errores)
# ============================================================


@db_session
def obtener_ingresos_totales_usuario(usuario_id: int, dias: int = 30) -> float:
    fecha_inicio = datetime.now().date() - timedelta(days=dias)
    ingresos = [
        i
        for i in list(Ingreso.select().order_by(Ingreso.id))
        if i.fk_usuarios.id == usuario_id and i.fecha >= fecha_inicio
    ]
    return float(sum(i.monto for i in ingresos))


@db_session
def obtener_egresos_totales_usuario(usuario_id: int, dias: int = 30) -> float:
    fecha_inicio = datetime.now().date() - timedelta(days=dias)
    egresos = [
        e
        for e in list(Egreso.select().order_by(Egreso.id))
        if e.fk_usuarios.id == usuario_id and e.fecha >= fecha_inicio
    ]
    return float(sum(e.monto for e in egresos))


@db_session
def obtener_egresos_por_categoria(
    usuario_id: int, categoria: str, dias: int = 30
) -> float:
    fecha_inicio = datetime.now().date() - timedelta(days=dias)
    categoria_lower = categoria.lower()
    egresos = [
        e
        for e in list(Egreso.select().order_by(Egreso.id))
        if e.fk_usuarios.id == usuario_id
        and e.fecha >= fecha_inicio
        and e.categoria.lower() == categoria_lower
    ]
    return float(sum(e.monto for e in egresos))


@db_session
def obtener_valor_total_activos(usuario_id: int) -> float:
    activos = [
        a
        for a in list(Activo.select().order_by(Activo.id))
        if a.fk_usuarios.id == usuario_id
    ]
    return float(sum(a.valor for a in activos))


@db_session
def obtener_flujo_mensual_activos(usuario_id: int) -> float:
    activos = [
        a
        for a in list(Activo.select().order_by(Activo.id))
        if a.fk_usuarios.id == usuario_id and a.flujo_mensual is not None
    ]
    return float(sum(a.flujo_mensual for a in activos if a.flujo_mensual))


@db_session
def obtener_total_deudas_mensuales(usuario_id: int) -> float:
    pasivos = [
        p
        for p in list(Pasivo.select().order_by(Pasivo.id))
        if p.fk_usuarios.id == usuario_id
    ]
    return float(sum(p.pago_mensual for p in pasivos))


@db_session
def obtener_total_deuda_pendiente(usuario_id: int) -> float:
    pasivos = [
        p
        for p in list(Pasivo.select().order_by(Pasivo.id))
        if p.fk_usuarios.id == usuario_id
    ]
    return float(sum(p.monto_total for p in pasivos))


@db_session
def obtener_categorias_usuario(usuario_id: int, dias: int = 30) -> List[Dict]:
    fecha_inicio = datetime.now().date() - timedelta(days=dias)
    egresos = [
        e
        for e in list(Egreso.select().order_by(Egreso.id))
        if e.fk_usuarios.id == usuario_id and e.fecha >= fecha_inicio
    ]
    categorias = {}
    for egreso in egresos:
        cat = egreso.categoria
        categorias[cat] = categorias.get(cat, 0) + egreso.monto
    return [{"categoria": k, "monto": v} for k, v in categorias.items()]


# ============================================================
# REGLAS DEL MOTOR DE INFERENCIA
# ============================================================


def regla_50_30_20(
    ingresos, egresos_necesidades, egresos_deseos, egresos_ahorros
) -> Dict:
    if ingresos == 0:
        return {
            "cumple": False,
            "mensaje": "No hay ingresos registrados",
            "severidad": "warning",
        }

    pct_necesidades = (egresos_necesidades / ingresos) * 100
    pct_deseos = (egresos_deseos / ingresos) * 100
    pct_ahorros = (egresos_ahorros / ingresos) * 100

    cumple = pct_necesidades <= 50 and pct_deseos <= 30 and pct_ahorros >= 20

    return {
        "cumple": cumple,
        "porcentajes": {
            "necesidades": round(pct_necesidades, 2),
            "deseos": round(pct_deseos, 2),
            "ahorros": round(pct_ahorros, 2),
        },
        "mensaje": (
            "✅ Cumples con la regla 50/30/20"
            if cumple
            else f"⚠️ No cumples: necesidades {pct_necesidades:.1f}%, deseos {pct_deseos:.1f}%, ahorros {pct_ahorros:.1f}%"
        ),
        "severidad": "success" if cumple else "warning",
    }


def regla_limite_endeudamiento(ingresos, deudas_mensuales) -> Dict:
    if ingresos == 0:
        return {
            "cumple": False,
            "mensaje": "No hay ingresos registrados",
            "severidad": "warning",
        }

    pct_deuda = (deudas_mensuales / ingresos) * 100
    cumple = pct_deuda <= 40
    nivel = "bajo" if pct_deuda < 30 else "medio" if pct_deuda <= 40 else "alto"

    return {
        "cumple": cumple,
        "porcentaje_deuda": round(pct_deuda, 2),
        "nivel_riesgo": nivel,
        "mensaje": f"Endeudamiento del {pct_deuda:.1f}%",
        "severidad": "success" if cumple else "danger",
    }


def regla_gasta_mas_que_gana(ingresos, egresos) -> Dict:
    if ingresos == 0:
        return {
            "cumple": False,
            "mensaje": "No hay ingresos registrados",
            "severidad": "danger",
        }

    cumple = egresos <= ingresos
    diferencia = ingresos - egresos
    return {
        "cumple": cumple,
        "diferencia": round(diferencia, 2),
        "mensaje": (
            f"✅ Ahorro mensual ${abs(diferencia):.2f}"
            if cumple
            else f"🚨 DÉFICIT: gastas ${abs(diferencia):.2f} más de lo que ganas"
        ),
        "severidad": "success" if cumple else "danger",
    }


def regla_fondo_emergencia(ingresos, ahorro_total) -> Dict:
    minimo, ideal = ingresos * 3, ingresos * 6
    if ahorro_total >= ideal:
        nivel = "excelente"
    elif ahorro_total >= minimo:
        nivel = "bueno"
    else:
        nivel = "insuficiente"
    return {
        "cumple": ahorro_total >= minimo,
        "nivel": nivel,
        "mensaje": f"Fondo actual ${ahorro_total:.2f}, mínimo ${minimo:.2f}, ideal ${ideal:.2f}",
        "severidad": (
            "success"
            if ahorro_total >= ideal
            else "warning" if ahorro_total >= minimo else "danger"
        ),
    }


def regla_sin_inversiones(valor_activos, flujo_mensual) -> Dict:
    tiene = valor_activos > 0
    return {
        "cumple": tiene,
        "mensaje": (
            "✅ Tienes activos" if tiene else "⚠️ No registras activos ni inversiones"
        ),
        "severidad": "success" if tiene else "warning",
    }


def regla_inversion_educacion(gastos_educacion, ingresos) -> Dict:
    if ingresos == 0:
        return {"cumple": False, "mensaje": "No hay ingresos", "severidad": "warning"}
    pct = (gastos_educacion / ingresos) * 100
    cumple = pct >= 5
    return {
        "cumple": cumple,
        "porcentaje": round(pct, 2),
        "mensaje": (
            f"✅ Inviertes {pct:.1f}% en educación"
            if cumple
            else f"⚠️ Inviertes {pct:.1f}%, recomendado 5%"
        ),
        "severidad": "success" if cumple else "warning",
    }


def regla_lujos_vs_educacion(gastos_lujos, gastos_educacion, valor_activos) -> Dict:
    cumple = gastos_lujos <= (gastos_educacion + valor_activos)
    return {
        "cumple": cumple,
        "mensaje": (
            "✅ Priorizas inversión productiva"
            if cumple
            else "⚠️ Gastas más en lujos que en educación o activos"
        ),
        "severidad": "success" if cumple else "warning",
    }


def regla_reserva_imprevistos(ingresos, ahorro_liquido) -> Dict:
    reserva_min = ingresos
    cumple = ahorro_liquido >= reserva_min
    return {
        "cumple": cumple,
        "mensaje": (
            f"✅ Tienes ${ahorro_liquido:.2f} de reserva"
            if cumple
            else f"⚠️ Te faltan ${reserva_min - ahorro_liquido:.2f} para 1 mes de reserva"
        ),
        "severidad": "success" if cumple else "warning",
    }


# ============================================================
# FUNCIÓN PRINCIPAL: EVALUAR SALUD FINANCIERA
# ============================================================


@db_session
def evaluar_salud_financiera(usuario_id: int, dias: int = 30) -> Dict:
    ingresos_totales = obtener_ingresos_totales_usuario(usuario_id, dias)
    egresos_totales = obtener_egresos_totales_usuario(usuario_id, dias)

    gastos_necesidades = sum(
        [
            obtener_egresos_por_categoria(usuario_id, c, dias)
            for c in ["vivienda", "comida", "transporte", "salud", "servicios"]
        ]
    )
    gastos_deseos = sum(
        [
            obtener_egresos_por_categoria(usuario_id, c, dias)
            for c in ["entretenimiento", "restaurantes", "viajes", "lujos"]
        ]
    )
    gastos_ahorros = obtener_egresos_por_categoria(usuario_id, "ahorro", dias)
    gastos_educacion = obtener_egresos_por_categoria(usuario_id, "educación", dias)
    gastos_lujos = obtener_egresos_por_categoria(usuario_id, "lujos", dias)
    ahorro_liquido = obtener_egresos_por_categoria(usuario_id, "ahorro", dias)

    valor_activos = obtener_valor_total_activos(usuario_id)
    flujo_activos = obtener_flujo_mensual_activos(usuario_id)
    deudas_mensuales = obtener_total_deudas_mensuales(usuario_id)
    deuda_total = obtener_total_deuda_pendiente(usuario_id)

    reglas = {
        "regla_50_30_20": regla_50_30_20(
            ingresos_totales, gastos_necesidades, gastos_deseos, gastos_ahorros
        ),
        "limite_endeudamiento": regla_limite_endeudamiento(
            ingresos_totales, deudas_mensuales
        ),
        "gasta_mas_que_gana": regla_gasta_mas_que_gana(
            ingresos_totales, egresos_totales
        ),
        "fondo_emergencia": regla_fondo_emergencia(
            ingresos_totales, gastos_ahorros * 6
        ),
        "sin_inversiones": regla_sin_inversiones(valor_activos, flujo_activos),
        "inversion_educacion": regla_inversion_educacion(
            gastos_educacion, ingresos_totales
        ),
        "lujos_vs_educacion": regla_lujos_vs_educacion(
            gastos_lujos, gastos_educacion, valor_activos
        ),
        "reserva_imprevistos": regla_reserva_imprevistos(
            ingresos_totales, ahorro_liquido
        ),
    }

    reglas_cumplidas = sum(1 for r in reglas.values() if r.get("cumple", False))
    total = len(reglas)

    return {
        "usuario_id": usuario_id,
        "resumen_financiero": {
            "ingresos": ingresos_totales,
            "egresos": egresos_totales,
            "balance": ingresos_totales - egresos_totales,
            "valor_activos": valor_activos,
            "deuda_total": deuda_total,
            "patrimonio_neto": valor_activos - deuda_total,
        },
        "reglas": reglas,
        "puntuacion_general": {
            "cumplidas": reglas_cumplidas,
            "total": total,
            "porcentaje": round((reglas_cumplidas / total) * 100, 2),
        },
    }
