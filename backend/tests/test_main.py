import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.database import Base, get_db
from app.main import app
from app.config import settings

# Use a test database for safety
TEST_DATABASE_URL = settings.database_url.replace("attendance_db", "test_attendance_db")

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestingSessionLocal() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Ibadan School Attendance System API is running"}

@pytest.mark.asyncio
async def test_create_classroom(client):
    response = await client.post("/classrooms/", json={"class_name": "SS1"})
    assert response.status_code == 200
    data = response.json()
    assert data["class_name"] == "SS1"
    assert "id" in data

@pytest.mark.asyncio
async def test_create_student(client):
    # First create a classroom
    class_res = await client.post("/classrooms/", json={"class_name": "SS1"})
    class_id = class_res.json()["id"]
    
    response = await client.post("/students/", json={
        "name": "Michael Philip",
        "student_id": "ADM-2026-001",
        "classroom_id": class_id
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Michael Philip"
    assert data["classroom_id"] == class_id

@pytest.mark.asyncio
async def test_mark_attendance(client):
    # Setup: classroom and student
    class_res = await client.post("/classrooms/", json={"class_name": "SS1"})
    class_id = class_res.json()["id"]
    student_res = await client.post("/students/", json={
        "name": "Michael Philip",
        "student_id": "ADM-2026-001",
        "classroom_id": class_id
    })
    student_id = student_res.json()["id"]
    
    # Test marking attendance
    response = await client.post("/attendance/", json={
        "student_id": student_id,
        "is_present": True
    })
    assert response.status_code == 200
    data = response.json()
    assert data["is_present"] is True
    assert data["student_id"] == student_id

@pytest.mark.asyncio
async def test_attendance_report(client):
    # Setup
    class_res = await client.post("/classrooms/", json={"class_name": "SS1"})
    class_id = class_res.json()["id"]
    student_res = await client.post("/students/", json={
        "name": "Michael Philip",
        "student_id": "ADM-2026-001",
        "classroom_id": class_id
    })
    student_id = student_res.json()["id"]
    await client.post("/attendance/", json={"student_id": student_id, "is_present": True})
    
    # Test report
    response = await client.get("/attendance/report/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["student_name"] == "Michael Philip"
    assert data[0]["is_present"] is True
