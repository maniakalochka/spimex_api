from fastapi import FastAPI
import uvicorn
from databases.db import init_db  # if you won't use alembic, call this function #
from api.routers import spimex_router


app =  FastAPI()

app.include_router(spimex_router)


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="localhost",
        port=8000,
        reload=True,
    )
