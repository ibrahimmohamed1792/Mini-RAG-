from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient 
from helpers.config import get_settings


app = FastAPI()
@app.on_event("starup")
async def startup_dp_client():
    settings=get_settings()

    app.mongo_conn=AsyncIOMotorClient(settings.MONGODB_URL) # type: ignore 
    app.db_client=app.mongo_conn[settings.MONGODB_DATABSE] # type: ignore 

@app.on_event("shutdown")

async def shutdown_db_client():
    app.mongo_conn.close() # type: ignore









app.include_router(base.base_router)
app.include_router(data.data_router)