from fastapi import APIRouter

import services

router = APIRouter()


@router.get("/{product_id}/")
async def hello(product_id: str):
    return await services.get_product_by_id(product_id)
