# PaperTrail Execution Guide

PaperTrail consists of three services. Open separate terminals from the project root:

---

### Terminal 1: Python AI Service
```powershell
cd ai-service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```
- **Health Check:** http://localhost:8001/internal/health
- **Swagger / Docs:** http://localhost:8001/docs

---

### Terminal 2: Java Spring Boot Backend
```powershell
cd backend-java
mvn spring-boot:run
```
- **Health Check:** http://localhost:8080/api/health
- **Swagger UI:** http://localhost:8080/swagger-ui/index.html

---

### Terminal 3: React Frontend (Vite / TanStack)
```powershell
cd frontend/paper
npm run dev
```
- **Web App:** http://localhost:3000
