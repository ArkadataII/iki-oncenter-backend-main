import sys
import logging
import uvicorn
from fastapi_jwt_auth import AuthJWT
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from app.routers.router import router
from app.models.base import BaseCustom
from app.db.base import engine
from app.helpers.config import Settings, settings

version = f"{sys.version_info.major}.{sys.version_info.minor}"

# Set up logging
formatter = logging.Formatter(fmt="[%(asctime)s][%(levelname)s] %(message)s", datefmt="%d-%m-%Y %H:%M:%S")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(stream_handler)

BaseCustom.metadata.create_all(bind=engine, checkfirst=True)


@AuthJWT.load_config
def get_config():
    return Settings()


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url='/api-docs',
        # docs_url=None,
        redoc_url=None,
        openapi_url=f"{settings.API_PREFIX}/api-identity.json",
        description='''ONCENTER PROJECTS''',
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)
    application.include_router(router, prefix=settings.API_PREFIX)

    @application.on_event("startup")
    async def startup_event():
        log.info(f'INITIALIZING APP API WITH PYTHON {version} ...')

    @application.on_event("shutdown")
    async def shutdown_event():
        log.info('SHUTTING DOWN APP API ...')

    return application


app = get_application()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000, debug=False, reload=False, workers=4)
