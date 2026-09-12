from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.routers import auth_router, protected, public

app = FastAPI(
    title="Supabase Auth API",
    description="FastAPI + Supabase JWT authentication with protected routes.",
    version="1.0.0",
)

app.include_router(auth_router.router)
app.include_router(protected.router)
app.include_router(public.router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Supabase Auth API",
        version="1.0.0",
        description="FastAPI + Supabase JWT authentication with protected routes.",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Paste your Supabase access_token here",
        }
    }

    for path in openapi_schema["paths"]:
        if "/protected/" in path:
            for method in openapi_schema["paths"][path]:
                openapi_schema["paths"][path][method]["security"] = [
                    {"BearerAuth": []}
                ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
