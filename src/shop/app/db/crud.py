from .mongodb import MongoManager


class ProductCrud:
    def __init__(self):
        mongo_manager = MongoManager()
        print(mongo_manager.db)
        print('*'*30)
        self.products = mongo_manager.db.get_collection('products')
        print(self.products)

    def product_collection(self):
        return self.products

    def create_product(self, product):
        return self.products.insert_one(product)

    def get_all_products(self):
        return self.products.find()

    async def get_product_by_id(self, product_id):
        print(111)
        print(product_id)
        result = await self.products.insert_one({"_id": product_id, 'name': 'hossein'})
        result = await self.products.find_one({"_id": product_id})
        print(result)
        print(2222)
        return result
