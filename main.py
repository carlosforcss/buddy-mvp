from fastapi import FastAPI, APIRouter
from src.files.routes import router as file_router


# 1. Create your FastAPI “app”
app = FastAPI(
    title="My UV-managed FastAPI App",
    version="0.1.0"
)


# 3. “Include” the router in the app
app.include_router(file_router)


if __name__ == "__main__":
    import uvicorn
    # 4. Run the app with Uvicorn
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
