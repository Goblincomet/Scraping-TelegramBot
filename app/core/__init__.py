from fastapi import FastAPI
import uvicorn
from starlette.responses import RedirectResponse
from core.manage import settings
from api.v1.controllers.telegram_bot_webhook import webhooks_router
from fastapi.middleware.cors import CORSMiddleware

origins = ["http://0.0.0.0:8000"]


def init_app():

    app = FastAPI(
        title="Telegram Bot API",
        description="a REST API using python for Telegram Bot",
        version="0.0.1",
        openapi_tags=settings.TAGS_METADATA,
        docs_url="/api-docs",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # Redirect
    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/api-docs")

    # Set global events
    async def startup_event():
        print('-- START API BOT TELEGRAM --')

    # execute global events
    @app.on_event("startup")
    async def on_startup():
        await startup_event()

    @app.on_event("shutdown")
    async def shutdown():
        print('Shutdown :c')

    # Routers
    app.include_router(webhooks_router, prefix="/api/v1")

    return app



app = init_app()


def start():
    uvicorn.run('core:app',host=settings.HOST,port=8000,reload=True)