from db.crud import ProductCrud


async def get_product_by_id(product_id):
    products_crud = ProductCrud()
    result = await products_crud.get_product_by_id(product_id)
    return result
