from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.utils import uuid_column


class Conversacion(Base):
    __tablename__ = "conversaciones"

    id         = uuid_column(primary_key=True)
    usuario_id = Column(String(36), ForeignKey("usuarios.id"), nullable=False)
    estado     = Column(String(20), nullable=False, default="activa")  # activa | cerrada
    inicio     = Column(DateTime, server_default=func.now())
    fin        = Column(DateTime, nullable=True)

    usuario  = relationship("Usuario", back_populates="conversaciones")
    mensajes = relationship("Mensaje", back_populates="conversacion", cascade="all, delete")