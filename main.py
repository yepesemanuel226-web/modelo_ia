from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app as _  # dispara la creación de tablas
from app.routes import usuarios, conversaciones, mensajes
from app.routes import citas, historial_clinico, diagnosticos, analisis_pnl

api = FastAPI(
    title="Centro Médico Virtual — API IA",
    description="API para el asistente médico con IA generativa (LLaMA 3.1 via Groq).",
    version="2.0.0"
)

# CORS — permite conexiones desde el cliente Java de escritorio
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas base
api.include_router(usuarios.router)
api.include_router(conversaciones.router)
api.include_router(mensajes.router)

# Rutas nuevas
api.include_router(citas.router)
api.include_router(historial_clinico.router)
api.include_router(diagnosticos.router)
api.include_router(analisis_pnl.router)


@api.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "mensaje": "Centro Médico Virtual API funcionando"}