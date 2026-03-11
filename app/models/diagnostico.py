from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.utils import uuid_column


class Diagnostico(Base):
    __tablename__ = "diagnosticos"

    id               = uuid_column(primary_key=True)
    conversacion_id  = Column(String(36), ForeignKey("conversaciones.id"), nullable=False)
    usuario_id       = Column(String(36), ForeignKey("usuarios.id"), nullable=False)
    contenido        = Column(Text, nullable=False)
    confianza        = Column(Float, nullable=True)
    created_at       = Column(DateTime, server_default=func.now())

    conversacion = relationship("Conversacion", foreign_keys=[conversacion_id])
    usuario      = relationship("Usuario", foreign_keys=[usuario_id])
