from typing import Annotated, Optional

from fastapi import APIRouter, Depends

from repository.repository_product import ProductRepository
from schemas.schemas_product import SProductAdd, SProduct, SProductId

router = APIRouter(
    prefix="/products",
    tags=["Товары(Продукты)"]
)

@router.post('')
async def add_product(
        product: Annotated[SProductAdd, Depends()],

) -> SProductId:
    product_id = await ProductRepository.add_one(product)
    return {"ok": True, "product_id": product_id}


@router.get('/{product_id}')
async def get_product_detail(
        product_id: Annotated[SProductId, Depends()]
) -> SProduct | str:
    product = await ProductRepository.get_one(product_id.product_id)
    return product


@router.get('')
async def get_products() -> Optional[list[SProduct]]:
    products = await ProductRepository.get_all()
    return products


@router.put('/{product_id}')
async def update_product_detail(
        product: Annotated[SProduct, Depends()]
) -> SProduct:
    updated_product = await ProductRepository.update_one(
        p_id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity
    )
    return updated_product


@router.delete('/{product_id}')
async def delete_product(
        product_id: Annotated[SProductId, Depends()]
) -> str:
    deleted_product = await ProductRepository.delete_one(p_id=product_id.product_id)
    return deleted_product

