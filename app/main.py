import uvicorn
from fastapi import FastAPI

from app.models.database import database, engine, metadata
from app.routers import boards, notes

metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(notes.router)
app.include_router(boards.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
