from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base
from app.utils import uuid_column


class AnalisisPNL(Base):
    __tablename__ = "analisis_pnl"

    id                = uuid_column(primary_key=True)
    conversacion_id   = Column(String(36), ForeignKey("conversaciones.id"), nullable=True)
    historial_id      = Column(String(36), ForeignKey("historial_paciente.id"), nullable=True)
    texto_original    = Column(Text, nullable=False)
    resumen           = Column(Text, nullable=True)
    entidades         = Column(JSONB, nullable=True)
    traduccion        = Column(Text, nullable=True)
    sentimiento       = Column(String(50), nullable=True)   # positivo | negativo | neutro
    score_sentimiento = Column(Float, nullable=True)
    idioma_detectado  = Column(String(20), nullable=True)
    created_at        = Column(DateTime, server_default=func.now())

    conversacion = relationship("Conversacion", foreign_keys=[conversacion_id])
