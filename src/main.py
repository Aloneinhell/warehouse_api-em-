from fastapi import FastAPI

from contextlib import asynccontextmanager

from database import create_tables, delete_tables
from routers.router_products import router as products_router
from routers.router_orders import router as orders_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print('База очищена')
    await create_tables()
    print('База готова')
    yield
    print('Выключение')


app = FastAPI(
    title='Warehouse',
    lifespan=lifespan
)
app.include_router(products_router)
app.include_router(orders_router)