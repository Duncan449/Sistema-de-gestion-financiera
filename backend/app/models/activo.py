from pony.orm import PrimaryKey, Required, Optional
from app.database.database import db


class Activo(db.Entity):
    _table_ = "activos"

    id = PrimaryKey(int, auto=True)
    valor = Required(float)
    tipo = Required(str)
    nombre = Required(str)
    flujo_mensual = Optional(float)
    fk_usuarios = Required("Usuario")  # Relación con Usuario, (clave foránea)
