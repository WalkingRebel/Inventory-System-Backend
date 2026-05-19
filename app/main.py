from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError
from app.core.database import Base, engine
from app.core.config import settings
from app.api.v1.router import api_router
from fastapi.exceptions import RequestValidationError
from app.core.exception_handlers import (
    validation_exception_handler,
    unhandled_exception_handler,
)

API_DESCRIPTION = """
Inventory Management System API for authentication, user access, product catalog management,
stock control, purchasing, sales, and reporting.

## Authentication
Send `Authorization: Bearer <token>` to access protected routes.

## Scope
- Authenticate users with JWT and optional Google OAuth.
- Manage users and role-protected operations.
- Create and list products.
- Adjust inventory and track stock movement.
- Record purchase and sales activity.
- Expose summary reporting endpoints.

## Version
Current API version: `v1` (`1.0.0`).

## Notes
- Most business routes are mounted under `/api/v1`.
- Protected endpoints require a bearer token in the `Authorization` header.
"""


OPENAPI_TAGS = [
    {
        "name": "auth",
        "description": "Authentication endpoints. Use these APIs to log in, start Google OAuth, and complete the OAuth callback flow.",
    },
    {
        "name": "users",
        "description": "User management and identity endpoints. These APIs create users, return the current authenticated user, and validate admin-only access.",
    },
    {
        "name": "products",
        "description": "Product catalog endpoints. Use these APIs to create new products and fetch the current list of products.",
    },
    {
        "name": "inventory",
        "description": "Inventory control endpoints. These APIs adjust stock quantities for products and support internal stock management workflows.",
    },
    {
        "name": "purchase",
        "description": "Purchase-order endpoints. Use these APIs to record inbound purchases and increase stock for purchased products.",
    },
    {
        "name": "sales",
        "description": "Sales-order endpoints. Use these APIs to record outbound sales and reduce stock for sold products.",
    },
    {
        "name": "reports",
        "description": "Reporting endpoints. These APIs return summary information about products, inventory, purchases, and sales.",
    },
]


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.DB_AUTO_CREATE:
        try:
            from app import models  # noqa: F401

            Base.metadata.create_all(bind=engine)
        except OperationalError as exc:
            raise RuntimeError(
                "Database connection failed. Set DATABASE_URL in .env (or disable DB_AUTO_CREATE)."
            ) from exc
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=API_DESCRIPTION,
    openapi_tags=OPENAPI_TAGS,
    swagger_ui_parameters={"persistAuthorization": True},
    lifespan=lifespan,
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get(
    "/",
    summary="Health welcome endpoint",
    description="Simple public endpoint that confirms the API is running.",
    tags=["root"],
)
def root():
    return {"message": "Welcome to Inventory Management System"}


