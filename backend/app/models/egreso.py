# app/models/egreso.py
from pony.orm import PrimaryKey, Required
from app.database.database import db
from datetime import date


class Egreso(db.Entity):
    _table_ = "egresos"

    id = PrimaryKey(int, auto=True)
    monto = Required(float)
    categoria = Required(str)
    fecha = Required(date)
    fk_usuarios = Required("Usuario")
