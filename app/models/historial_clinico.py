from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.utils import uuid_column


class HistorialClinico(Base):
    __tablename__ = "historial_clinico"

    id          = uuid_column(primary_key=True)
    usuario_id  = Column(String(36), ForeignKey("usuarios.id"), nullable=False)
    medico_id   = Column(String(36), ForeignKey("usuarios.id"), nullable=True)
    titulo      = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=False)
    fecha       = Column(DateTime, server_default=func.now())

    usuario = relationship("Usuario", foreign_keys=[usuario_id])
    medico  = relationship("Usuario", foreign_keys=[medico_id])
