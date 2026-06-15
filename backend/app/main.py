from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from . import crud, schemas, models
from .database import engine, Base, get_db

app = FastAPI(title="Ibadan School Attendance System")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/classrooms/", response_model=schemas.Classroom)
async def create_classroom(classroom: schemas.ClassroomCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_classroom(db=db, classroom=classroom)

@app.post("/students/", response_model=schemas.Student)
async def create_student(student: schemas.StudentCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_student(db=db, student=student)

@app.get("/students/", response_model=List[schemas.Student])
async def read_students(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_students(db, skip=skip, limit=limit)

@app.post("/attendance/", response_model=schemas.Attendance)
async def mark_attendance(attendance: schemas.AttendanceCreate, db: AsyncSession = Depends(get_db)):
    return await crud.mark_attendance(db=db, attendance=attendance)

@app.get("/attendance/report/")
async def read_attendance_report(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    report = await crud.get_attendance_report(db, skip=skip, limit=limit)
    return [
        {"student_name": row.student_name, "is_present": row.Attendance.is_present, "timestamp": row.Attendance.timestamp}
        for row in report
    ]

@app.get("/")
async def root():
    return {"message": "Ibadan School Attendance System API is running"}
