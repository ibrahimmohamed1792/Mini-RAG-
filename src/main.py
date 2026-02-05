from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient 
from helpers.config import get_settings


app = FastAPI()

async def startup_db_client():
    settings=get_settings()

    app.mongo_conn=AsyncIOMotorClient(settings.MONGODB_URL)  
    app.db_client=app.mongo_conn[settings.MONGODB_DATABSE]  



async def shutdown_db_client():
    app.mongo_conn.close() # type: ignore







app.router.lifespan.on_startup.append(startup_db_client)
app.router.lifespan.on_shutdown.append(shutdown_db_client)

app.include_router(base.base_router)
app.include_router(data.data_router)