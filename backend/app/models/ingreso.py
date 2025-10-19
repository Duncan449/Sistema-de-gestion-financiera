# app/models/ingreso.py
from pony.orm import PrimaryKey, Required
from app.database.database import db
from datetime import date  # para el tipo DATE


class Ingreso(db.Entity):
    _table_ = "ingresos"

    id = PrimaryKey(int, auto=True)
    monto = Required(float)
    categoria = Required(str)
    fecha = Required(date)
    fk_usuarios = Required("Usuario")  # Relación con Usuario, (clave foránea)
