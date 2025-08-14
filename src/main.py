import uvicorn
from fastapi import FastAPI

from api.routers import router
from middlewares.redis_mw import RedisCacheMiddleware

app = FastAPI()

app.add_middleware(RedisCacheMiddleware)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="localhost",
        port=8000,
        reload=True,
    )
