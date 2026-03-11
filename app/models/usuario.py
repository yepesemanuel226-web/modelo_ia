from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.utils import uuid_column


class Usuario(Base):
    __tablename__ = "usuarios"

    id             = uuid_column(primary_key=True)
    nombre         = Column(String(100), nullable=False)
    email          = Column(String(150), unique=True, nullable=True)
    rol            = Column(String(30), nullable=False, default="paciente")  # paciente | medico
    activo         = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, server_default=func.now())

    conversaciones   = relationship("Conversacion", back_populates="usuario", cascade="all, delete")
    historial_clinico = relationship("HistorialClinico", back_populates="usuario", cascade="all, delete")
    historial_paciente = relationship("HistorialPaciente", back_populates="usuario", cascade="all, delete")