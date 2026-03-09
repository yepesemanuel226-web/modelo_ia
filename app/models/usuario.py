from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid


class Usuario(Base):
    __tablename__ = "usuarios"

    id             = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre         = Column(String(100), nullable=False)
    email          = Column(String(150), unique=True, nullable=True)
    rol            = Column(String(30), nullable=False, default="paciente")  # paciente | medico
    activo         = Column(Boolean, default=True)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())

    conversaciones = relationship("Conversacion", back_populates="usuario", cascade="all, delete")
