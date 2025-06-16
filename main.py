from fastapi import FastAPI
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
from src.routes.files import router as file_router
from src.routes.voice import router as audio_router
from src.routes.conversations import router as conversations_router
from config.settings import SENTRY_DSN
from fastapi.responses import JSONResponse
from tortoise.exceptions import DBConnectionError


def get_app(*args):
    # Initialize Sentry if DSN is available
    if SENTRY_DSN:
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[FastApiIntegration()],
            send_default_pii=True,
        )

    app = FastAPI(
        title="Buddy API helps to implement real-life accessibility", version="0.1.0"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    @app.get("/alive")
    async def alive():
        return {"status": "alive"}

    @app.get("/sentry-debug")
    async def trigger_error():
        division_by_zero = 1 / 0

    # 3. "Include" the router in the app
    app.include_router(file_router)
    app.include_router(audio_router)
    app.include_router(conversations_router)

    register_tortoise(
        app,
        db_url="sqlite://db.sqlite3",
        modules={
            "models": [
                "src.models",
            ]
        },
        generate_schemas=True,
        add_exception_handlers=True,
    )

    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:get_app",
        reload=True,
        host="0.0.0.0",
        port=8000,
        factory=True,
        reload_dirs=["src"],
    )
