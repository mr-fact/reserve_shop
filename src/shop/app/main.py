import uvicorn
from fastapi import FastAPI

from api import router
import settings
from db.mongodb import MongoManager
from db import settings as db_settings


def get_application():
    application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION,
    )
    application.include_router(router, prefix=settings.PREFIX)
    return application


app = get_application()


@app.on_event("startup")
async def startup_db_client():
    mongo_manager = MongoManager()
    mongo_manager.connect(db_settings.mongo_settings.mongo_url)


@app.on_event("shutdown")
async def shutdown_db_client():
    mongo_manager = MongoManager()
    mongo_manager.disconnect()


if __name__ == "__main__":
    uvicorn.run('main:app', host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
