from fastapi import FastAPI
import uvicorn
from api.routers import spimex_router


app =  FastAPI()

app.include_router(spimex_router)

from models.base import Base
from databases.db import engine  # предполагается, что engine уже настроен


if __name__ == "__main__":

    uvicorn.run(
        app=app,
        host="localhost",
        port=8001,
        reload=True,
    )
