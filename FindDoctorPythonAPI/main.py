from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import init_db
from csharp_client import csharp_client
from config import settings

# Importar routers
from routers import edit_suggestions, doctors, appointments, csharp_proxy

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia startup e shutdown da aplicação"""
    # Startup
    print("🚀 Iniciando FindDoctor Python API...")
    print(f"📦 Criando tabelas no banco: {settings.DATABASE_NAME}...")
    init_db()
    print("✅ API pronta!")
    
    yield
    
    # Shutdown
    print("🔌 Fechando conexões...")
    await csharp_client.close()
    print("👋 API encerrada!")

app = FastAPI(
    title="FindDoctor Python API",
    description="API para sistema de edições e agendamentos do FindDoctor",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],  # FindDoctorNewFrontEnd + FrontEndAgendamento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(edit_suggestions.router, prefix="/api")
app.include_router(doctors.router, prefix="/api")
app.include_router(appointments.router, prefix="/api")
app.include_router(csharp_proxy.router, prefix="/api")

@app.get("/")
def root():
    """Endpoint raiz"""
    return {
        "message": "FindDoctor Python API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "edit_suggestions": "/api/edit-suggestions",
            "doctors": "/api/doctors",
            "appointments": "/api/appointments",
            "csharp_proxy": "/api/csharp"
        }
    }

@app.get("/health")
def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "database": settings.DATABASE_NAME,
        "csharp_api": settings.CSHARP_API_URL
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )
