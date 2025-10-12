# app/database/database.py
from pony.orm import Database
from dotenv import load_dotenv
import os

load_dotenv()

# Crear instancia de la base de datos
db = Database()


def init_database():
    """
    Inicializa la conexión con Pony ORM
    """
    try:
        DATABASE_URL = os.getenv("DATABASE_URL")

        # Bind con PostgreSQL
        db.bind(provider="postgres", dsn=DATABASE_URL)

        # Generar mapeo (sin crear tablas porque ya existen)
        db.generate_mapping(create_tables=False)

        print("✅ Base de datos conectada correctamente")

    except Exception as e:
        print(f"❌ Error al conectar con la base de datos: {e}")
        raise e
