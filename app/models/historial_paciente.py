from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.utils import uuid_column


class HistorialPaciente(Base):
    __tablename__ = "historial_paciente"

    id          = uuid_column(primary_key=True)
    usuario_id  = Column(String(36), ForeignKey("usuarios.id"), nullable=False)
    descripcion = Column(Text, nullable=False)
    creado_en   = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("Usuario", back_populates="historial_paciente")