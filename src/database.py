import datetime
from sqlalchemy import func, ForeignKey

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


engine = create_async_engine(
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class ProductOrm(Model):
    __tablename__ = "Products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    quantity: Mapped[int]


class OrderOrm(Model):
    __tablename__ = "Orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    date_of_creation: Mapped[datetime.datetime] = mapped_column(insert_default=func.now())
    status: Mapped[str]


class OrderItemOrm(Model):
    __tablename__ = "OrderItem"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('Orders.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey("Products.id"))
    quantity_of_product: Mapped[int]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)