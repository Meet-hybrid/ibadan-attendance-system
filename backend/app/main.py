from fastapi import FastAPI
from .database import engine, Base

app = FastAPI(title="Ibadan School Attendance System")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Ibadan School Attendance System API"}
