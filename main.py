from fastapi import FastAPI
from api_routes.endpoints.products import router as products_router
from api_routes.endpoints.sales import router as sales_router
from api_routes.endpoints.inventory import router as inventory_router
from api_routes.endpoints.revenue import router as revenue_router


app = FastAPI()

# Include routers

app.include_router(products_router, prefix="/api_routes", tags=["products"])
app.include_router(sales_router, prefix="/api_routes", tags=["sales"])
app.include_router(inventory_router, prefix="/api_routes", tags=["inventory"])
app.include_router(revenue_router, prefix="/api_routes" , tags=["revenue"])


