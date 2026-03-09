from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.utils import uuid_column


class Mensaje(Base):
    __tablename__ = "mensajes"

    id              = uuid_column(primary_key=True)
    conversacion_id = Column(String(36), ForeignKey("conversaciones.id"), nullable=False)
    rol             = Column(String(20), nullable=False)  # usuario | asistente
    contenido       = Column(Text, nullable=False)
    fecha_mensaje   = Column(DateTime, server_default=func.now())

    conversacion = relationship("Conversacion", back_populates="mensajes")