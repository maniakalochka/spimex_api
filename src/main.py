from fastapi import FastAPI
import uvicorn


app =  FastAPI()


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="localhost",
        port=8000,
        reload=True,
    )
