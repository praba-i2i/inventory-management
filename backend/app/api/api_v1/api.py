from fastapi import APIRouter
from app.api.api_v1.endpoints import items, categories, products, inventory, suppliers, locations, purchase_orders, stock_alerts

api_router = APIRouter()

api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["suppliers"])
api_router.include_router(locations.router, prefix="/locations", tags=["locations"])
api_router.include_router(purchase_orders.router, prefix="/purchase-orders", tags=["purchase-orders"])
api_router.include_router(stock_alerts.router, prefix="/stock-alerts", tags=["stock-alerts"])
