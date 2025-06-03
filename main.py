from fastapi import FastAPI
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
from src.files.routes import router as file_router
from src.voice.routes import router as audio_router
from src.conversations.routes import router as conversations_router
from config.db import initialize_db


def get_app(*args):
    app = FastAPI(
        title="Buddy API helps to implement real-life accessibility", 
        version="0.1.0"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    # 3. "Include" the router in the app
    app.include_router(file_router)
    app.include_router(audio_router)
    app.include_router(conversations_router)

    register_tortoise(
        app,
        db_url="sqlite://db.sqlite3",
        modules={
            "models": [
                "src.files.models",
                "src.conversations.models",
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

