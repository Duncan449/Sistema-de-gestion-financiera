# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

# Importar modelo ANTES de init_database
from app.models.usuario import Usuario
from app.models.ingreso import Ingreso
from app.models.egreso import Egreso
from app.models.pasivo import Pasivo

# Importar e inicializar base de datos
from app.database.database import init_database

init_database()

# Importar rutas
from app.routes import usuarioRoutes, ingresoRoutes, egresoRoutes, authRoutes, pasivoRoutes

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
app.include_router(authRoutes.router)
app.include_router(usuarioRoutes.router)
app.include_router(ingresoRoutes.router)
app.include_router(egresoRoutes.router)
app.include_router(pasivoRoutes.router)


# Configurar OpenAPI para mostrar seguridad Bearer
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Sistema Experto Financiero - API",
        version="1.0.0",
        description="API para gestión de usuarios con autenticación JWT",
        routes=app.routes,
    )

    # Agregar esquema de seguridad Bearer
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Ingresa tu token JWT",
        }
    }

    # Aplicar seguridad a todos los endpoints menos /auth/login y /auth/register
    for path, path_item in openapi_schema["paths"].items():
        if (
            "/auth/login" not in path
            and "/auth/register" not in path
            and "/auth/login-form" not in path
        ):
            for operation in path_item.values():
                if isinstance(operation, dict):
                    operation.setdefault("security", []).append({"Bearer": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
