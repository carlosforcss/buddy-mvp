from fastapi import FastAPI
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise
from src.files.routes import router as file_router
from src.voice.routes import router as audio_router
from src.conversations.routes import router as conversations_router
from config.db import initialize_db


app = FastAPI(
    title="Buddy API helps to implement real-life accessibility",
    version="0.1.0"
)


# 3. “Include” the router in the app
app.include_router(file_router)
app.include_router(audio_router)
app.include_router(conversations_router)

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["src.files.models.files"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        reload=True, 
        host="0.0.0.0", 
        port=8000
    )

