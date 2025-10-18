# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar modelo ANTES de init_database
from app.models.usuario import Usuario
from app.models.egreso import Egreso  

# Importar e inicializar base de datos
from app.database.database import init_database

init_database()

# Importar rutas
from app.routes import usuarioRoutes, egresoRoutes 

# Crear app
app = FastAPI(
    title="Sistema Experto Financiero - API",
    version="1.0.0",
    description="API para gestión de usuarios y egresos con Pony ORM",
)

# Configurar CORS (opcional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Ruta raíz
@app.get("/")
def root():
    return {
        "mensaje": "API del Sistema Experto Financiero",
        "status": "funcionando correctamente",
        "version": "1.0.0",
    }

# Incluir rutas
app.include_router(usuarioRoutes.router)
app.include_router(egresoRoutes.router)
