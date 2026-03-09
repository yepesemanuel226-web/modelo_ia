from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app as _  # dispara la creación de tablas
from app.routes import usuarios, conversaciones, mensajes

api = FastAPI(
    title="Centro Médico Virtual — API IA",
    description="API para el asistente médico con IA generativa (LLaMA 3.1 via Groq).",
    version="1.0.0"
)

# CORS — permite conexiones desde el cliente Python de escritorio
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rutas
api.include_router(usuarios.router)
api.include_router(conversaciones.router)
api.include_router(mensajes.router)


@api.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "mensaje": "Centro Médico Virtual API funcionando"}
