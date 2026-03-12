from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


# ──────────────────────────────────────────────
# CITAS MÉDICAS
# ──────────────────────────────────────────────
class CitaCrear(BaseModel):
    paciente_id: str
    medico_id:   str
    fecha_cita:  datetime
    motivo:      str
    notas:       Optional[str] = None

class CitaActualizar(BaseModel):
    estado: Optional[str] = None
    notas:  Optional[str] = None

class CitaRespuesta(BaseModel):
    id:          UUID
    paciente_id: UUID
    medico_id:   UUID
    fecha_cita:  datetime
    motivo:      str
    estado:      str
    notas:       Optional[str]
    created_at:  datetime

    class Config:
        from_attributes = True


# ──────────────────────────────────────────────
# HISTORIAL CLÍNICO
# ──────────────────────────────────────────────
class HistorialClinicoCrear(BaseModel):
    usuario_id:  str
    medico_id:   Optional[str] = None
    titulo:      str
    descripcion: str

class HistorialClinicoRespuesta(BaseModel):
    id:          UUID
    usuario_id:  UUID
    medico_id:   Optional[UUID]
    titulo:      Optional[str]
    descripcion: Optional[str]
    fecha:       Optional[datetime]

    class Config:
        from_attributes = True


# ──────────────────────────────────────────────
# DIAGNÓSTICOS
# ──────────────────────────────────────────────
class DiagnosticoCrear(BaseModel):
    conversacion_id: str
    usuario_id:      str
    contenido:       str
    confianza:       Optional[float] = None

class DiagnosticoRespuesta(BaseModel):
    id:              UUID
    conversacion_id: UUID
    usuario_id:      UUID
    contenido:       str
    confianza:       Optional[float]
    created_at:      datetime

    class Config:
        from_attributes = True


# ──────────────────────────────────────────────
# ANÁLISIS PNL
# ──────────────────────────────────────────────
class AnalisisPNLCrear(BaseModel):
    conversacion_id:   Optional[str] = None
    historial_id:      Optional[str] = None
    texto_original:    str
    resumen:           Optional[str] = None
    entidades:         Optional[dict] = None
    traduccion:        Optional[str] = None
    sentimiento:       Optional[str] = None
    score_sentimiento: Optional[float] = None
    idioma_detectado:  Optional[str] = None

class AnalisisPNLRespuesta(BaseModel):
    id:                UUID
    conversacion_id:   Optional[UUID]
    historial_id:      Optional[UUID]
    texto_original:    str
    resumen:           Optional[str]
    entidades:         Optional[dict]
    traduccion:        Optional[str]
    sentimiento:       Optional[str]
    score_sentimiento: Optional[float]
    idioma_detectado:  Optional[str]
    created_at:        datetime

    class Config:
        from_attributes = True