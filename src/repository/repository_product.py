from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound

from database import new_session, ProductOrm
from schemas.schemas_product import SProductAdd, SProduct


class ProductRepository:
    @classmethod
    async def add_one(cls, data: SProductAdd) -> int:
        async with new_session() as session:
            product_dict = data.model_dump()
            product = ProductOrm(**product_dict)
            session.add(product)
            await session.flush()
            await session.commit()
            return product.id

    @classmethod
    async def get_all(cls) -> list[SProduct]:
        async with new_session() as session:
            query = select(ProductOrm)
            result = await session.execute(query)
            print(result)
            product_models = result.scalars().all()
            print(product_models)
            product_schemas = [SProduct.model_validate(product_model) for product_model in product_models]
            return product_schemas

    @classmethod
    async def get_one(cls, p_id) -> Optional[SProduct] | str:
        async with new_session() as session:
            try:
                query = select(ProductOrm).filter(ProductOrm.id == p_id)
                result = await session.execute(query)
                product_model = result.scalars().one()
                product_schema = SProduct.model_validate(product_model)
                return product_schema
            except NoResultFound:
                raise HTTPException(status_code=404, detail=f"Нет товара с id {p_id}")

    @classmethod
    async def update_one(
            cls, p_id, name, description, price, quantity
    ) -> SProduct:
        async with new_session() as session:
            try:
                query = select(ProductOrm).filter(ProductOrm.id == p_id)
                result = await session.execute(query)
                product_model = result.scalars().one()

                stmnt = (
                    update(ProductOrm).
                    where(ProductOrm.id == p_id).
                    values(
                        name=name,
                        description=description,
                        price=price,
                        quantity=quantity
                    )

                )
                await session.execute(stmnt)
                await session.commit()
                product_schema = SProduct.model_validate(product_model)
                return product_schema
            except NoResultFound:
                raise HTTPException(status_code=404, detail=f"Нет товара с id {p_id}")

    @classmethod
    async def delete_one(cls, p_id) -> str:
        async with new_session() as session:
            try:
                query = select(ProductOrm).filter(ProductOrm.id == p_id)
                result = await session.execute(query)
                result.scalars().one()



                stmt = (
                    delete(ProductOrm).
                    where(ProductOrm.id == p_id)
                )

                await session.execute(stmt)
                await session.commit()
                return f"Товар с id {p_id} успешно удален!"
            except NoResultFound:
                raise HTTPException(status_code=404, detail=f"Нет товара с id {p_id}")





