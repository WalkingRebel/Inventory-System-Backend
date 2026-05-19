from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    inventory,
    products,
    purchase,
    reports,
    sales,
    users,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(purchase.router, prefix="/purchase", tags=["purchase"])
api_router.include_router(sales.router, prefix="/sales", tags=["sales"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
