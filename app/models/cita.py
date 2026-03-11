from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.utils import uuid_column, fk_uuid_column


class Cita(Base):
    __tablename__ = "citas_medicas"

    id          = uuid_column(primary_key=True)
    paciente_id = fk_uuid_column("usuarios.id")
    medico_id   = fk_uuid_column("usuarios.id")
    fecha_cita  = Column(DateTime, nullable=False)
    motivo      = Column(Text, nullable=False)
    estado      = Column(String(20), nullable=False, default="pendiente")
    notas       = Column(Text, nullable=True)
    created_at  = Column(DateTime, server_default=func.now())
    updated_at  = Column(DateTime, server_default=func.now(), onupdate=func.now())

    paciente = relationship("Usuario", foreign_keys="Cita.paciente_id")
    medico   = relationship("Usuario", foreign_keys="Cita.medico_id")