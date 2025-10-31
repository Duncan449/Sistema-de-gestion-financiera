# app/models/ingreso.py
# Modelo ORM que representa la tabla 'pasivos' en la base de datos
from pony.orm import PrimaryKey, Required
from app.database.database import db
from datetime import date  


class Pasivo(db.Entity):

    """
    Entidad que representa un pasivo financiero (deuda, préstamo, etc.)
    Mapea a la tabla 'pasivos' en PostgreSQL
    
    """

    _table_ = "pasivos"

    id = PrimaryKey(int, auto=True)
    nombre = Required(str)
    tipo = Required(str)
    monto_total = Required(float)
    pago_mensual = Required(float)
    fecha_vencimiento = Required(date)
    fk_usuarios = Required("Usuario")  # Relación con usuarios, (clave foránea)
    