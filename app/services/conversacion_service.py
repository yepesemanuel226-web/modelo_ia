from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app.models.conversacion import Conversacion
from uuid import UUID


class ConversacionService:
    """Gestión del ciclo de vida de las conversaciones."""

    def __init__(self, db: Session):
        self.db = db

    def crear(self, usuario_id) -> Conversacion:
        conversacion = Conversacion(
            usuario_id=str(usuario_id),  # convertir a str para SQLite
            estado="activa"
        )
        self.db.add(conversacion)
        self.db.commit()
        self.db.refresh(conversacion)
        return conversacion

    def obtener_activa_por_usuario(self, usuario_id) -> Conversacion:
        return self.db.query(Conversacion).filter(
            Conversacion.usuario_id == str(usuario_id),
            Conversacion.estado == "activa"
        ).first()

    def obtener_por_id(self, conversacion_id) -> Conversacion:
        conv = self.db.query(Conversacion).filter(
            Conversacion.id == str(conversacion_id)
        ).first()
        if not conv:
            raise HTTPException(status_code=404, detail="Conversación no encontrada")
        return conv

    def obtener_por_usuario(self, usuario_id) -> list[Conversacion]:
        return self.db.query(Conversacion).filter(
            Conversacion.usuario_id == str(usuario_id)
        ).order_by(Conversacion.inicio.desc()).all()

    def cerrar(self, conversacion_id) -> Conversacion:
        conv = self.obtener_por_id(conversacion_id)
        if conv.estado == "cerrada":
            raise HTTPException(status_code=400, detail="La conversación ya está cerrada")
        conv.estado = "cerrada"
        conv.fin = datetime.utcnow()
        self.db.commit()
        self.db.refresh(conv)
        return conv