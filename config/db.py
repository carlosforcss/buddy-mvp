from tortoise import Tortoise


async def initialize_db():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3", modules={"models": ["src.files.models"]}
    )
    await Tortoise.generate_schemas()
