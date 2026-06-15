# Ibadan Secondary School Attendance System

A human-centered, robust student attendance system tailored for the Nigerian educational ecosystem, specifically designed for secondary schools in Ibadan.

## 🚀 Overview
This system addresses the challenges of manual attendance recording in local schools, such as record falsification and communication gaps with parents. It features an **Offline-First** architecture to handle inconsistent connectivity and provides **Real-Time Notifications** for administrators and parents.

## 🛠️ Technical Stack
- **Backend:** FastAPI (Python 3.10+)
- **Database:** MySQL (Primary) with asynchronous `aiomysql` driver
- **ORM:** SQLAlchemy (Async)
- **Real-Time:** WebSockets for instant attendance alerts
- **Configuration:** Pydantic Settings with `.env` support
- **Testing:** Pytest with Async support

## 📂 Project Structure
- `backend/app/`: Core application logic (models, schemas, crud, websockets).
- `backend/tests/`: Comprehensive test suite.
- `docs/`: Technical design and discovery documents.

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.10+
- MySQL Server

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlalchemy aiomysql pydantic-settings httpx pytest pytest-asyncio
   ```
4. Create a `.env` file based on the design:
   ```env
   DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/attendance_db
   SECRET_KEY=your-secret-key
   DEBUG=True
   ```
5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## 🧪 Running Tests
```bash
cd backend
pytest
```

## 📜 Key Features
- **Asynchronous Database Operations:** High-performance MySQL integration.
- **Pydantic Validation:** Strict data integrity for all inputs.
- **WebSocket Broadcast:** Instant notifications when attendance is marked.
- **Clean Architecture:** Self-documenting code following industry standards.
