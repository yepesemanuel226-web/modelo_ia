from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.schemas import ConversacionRespuesta
from app.services import ConversacionService

router = APIRouter(prefix="/conversaciones", tags=["Conversaciones"])


@router.get("/usuario/{usuario_id}", response_model=list[ConversacionRespuesta])
def historial_conversaciones(usuario_id: UUID, db: Session = Depends(get_db)):
    """Lista todas las conversaciones de un usuario (para el módulo Seguimiento del médico)."""
    return ConversacionService(db).obtener_por_usuario(usuario_id)


@router.put("/cerrar/{conversacion_id}", response_model=ConversacionRespuesta)
def cerrar_conversacion(conversacion_id: UUID, db: Session = Depends(get_db)):
    """Cierra una conversación activa."""
    return ConversacionService(db).cerrar(conversacion_id)
