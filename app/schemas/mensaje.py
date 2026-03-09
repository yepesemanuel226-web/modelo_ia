from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from uuid import UUID


class MensajeRespuesta(BaseModel):
    id:              UUID
    conversacion_id: UUID
    rol:             str
    contenido:       str
    fecha_mensaje:   datetime

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    """Payload que el cliente envía para chatear con el asistente médico."""
    usuario_id: UUID = Field(..., example="550e8400-e29b-41d4-a716-446655440000")
    mensaje:    str  = Field(..., min_length=1, max_length=2000,
                             example="Tengo dolor de cabeza fuerte desde hace 2 días")

    @field_validator("mensaje")
    @classmethod
    def mensaje_no_vacio(cls, v):
        if not v.strip():
            raise ValueError("El mensaje no puede estar vacío")
        return v.strip()


class ChatResponse(BaseModel):
    """Respuesta del asistente médico IA."""
    conversacion_id: UUID
    respuesta:       str

    class Config:
        from_attributes = True
