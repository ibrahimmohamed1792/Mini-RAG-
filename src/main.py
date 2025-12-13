from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient 


app = FastAPI()
app.include_router(base.base_router)
app.include_router(data.data_router)