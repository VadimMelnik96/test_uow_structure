from fastapi import FastAPI


from app.adapters.api.http.v1.routers.customer_router import router
from app.settings.settings import config


def create_app() -> FastAPI:
    """Генерация приложения"""
    application = FastAPI(title=config.app.name
    )
    application.include_router(router)
    return application


app = create_app()
