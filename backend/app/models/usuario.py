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
    ingresos = Set("Ingreso")  # Relación inversa para la FK (un usuario puede tener muchos ingresos)
    egresos = Set("Egreso")
    pasivos = Set("Pasivo")
