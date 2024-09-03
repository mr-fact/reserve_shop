import motor.motor_asyncio


class MongoManager:
    client = None
    db = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MongoManager, cls).__new__(cls)
        return cls.instance

    def connect(self, url):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(url)
        self.db = self.client.reserve_shop

    def disconnect(self):
        self.client.close()
