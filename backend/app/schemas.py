from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class ClassroomBase(BaseModel):
    class_name: str = Field(..., example="Senior Secondary 1 (SS1)")

class ClassroomCreate(ClassroomBase):
    pass

class Classroom(ClassroomBase):
    id: int
    
    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    name: str = Field(..., example="Michael Philip")
    student_id: str = Field(..., example="ADM-2026-001")
    classroom_id: int

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    
    class Config:
        from_attributes = True

class AttendanceBase(BaseModel):
    student_id: int
    is_present: bool
    timestamp: datetime = Field(default_factory=datetime.now)

class AttendanceCreate(AttendanceBase):
    pass

class Attendance(AttendanceBase):
    id: int
    
    class Config:
        from_attributes = True

class AttendanceSummary(BaseModel):
    student_name: str
    is_present: bool
    timestamp: datetime
