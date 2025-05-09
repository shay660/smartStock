from fastapi import FastAPI
import uvicorn

from backend.routers import auth
from backend.database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
