import uvicorn
from fastapi import FastAPI

from api import router
import settings


# without this we can't run the project from a docker container
# we have to add the parent folder to sys.path
# from os.path import abspath, dirname
# parent_path = dirname(dirname(abspath(__file__)))
# sys.path.append(parent_path)


def get_application():
    application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION,
    )
    application.include_router(router, prefix=settings.PREFIX)
    return application


app = get_application()
if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=settings.DEBUG)
