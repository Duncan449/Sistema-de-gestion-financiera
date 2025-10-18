# app/models/usuario.py
from pony.orm import PrimaryKey, Required, Set
from app.database.database import db


class Usuario(db.Entity):
    _table_ = "usuarios"

    id = PrimaryKey(int, auto=True)
    nombre_completo = Required(str)
    password = Required(str)
    email = Required(str)
    username = Required(str)
    egresos = Set("Egreso")
