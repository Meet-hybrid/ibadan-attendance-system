from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from . import models, schemas

async def get_student(db: AsyncSession, student_id: int):
    result = await db.execute(select(models.Student).filter(models.Student.id == student_id))
    return result.scalars().first()

async def get_students(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Student).offset(skip).limit(limit))
    return result.scalars().all()

async def create_student(db: AsyncSession, student: schemas.StudentCreate):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student

async def create_classroom(db: AsyncSession, classroom: schemas.ClassroomCreate):
    db_classroom = models.Classroom(**classroom.model_dump())
    db.add(db_classroom)
    await db.commit()
    await db.refresh(db_classroom)
    return db_classroom

async def mark_attendance(db: AsyncSession, attendance: schemas.AttendanceCreate):
    db_attendance = models.Attendance(**attendance.model_dump())
    db.add(db_attendance)
    await db.commit()
    await db.refresh(db_attendance)
    return db_attendance

async def get_attendance_report(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.Attendance, models.Student.name.label("student_name"))
        .join(models.Student)
        .offset(skip)
        .limit(limit)
    )
    return result.all()
