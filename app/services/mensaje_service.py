from sqlalchemy.orm import Session
from app.models.mensaje import Mensaje
from uuid import UUID


class MensajeService:
    """Almacenamiento y consulta del historial de mensajes."""

    def __init__(self, db: Session):
        self.db = db

    def guardar(self, conversacion_id: UUID, rol: str, contenido: str) -> Mensaje:
        mensaje = Mensaje(
            conversacion_id=conversacion_id,
            rol=rol,
            contenido=contenido
        )
        self.db.add(mensaje)
        self.db.commit()
        self.db.refresh(mensaje)
        return mensaje

    def obtener_historial(self, conversacion_id: UUID) -> list[Mensaje]:
        return self.db.query(Mensaje).filter(
            Mensaje.conversacion_id == conversacion_id
        ).order_by(Mensaje.fecha_mensaje).all()

    def obtener_historial_como_dict(self, conversacion_id: UUID) -> list[dict]:
        """Retorna el historial en formato compatible con la API de Groq."""
        mensajes = self.obtener_historial(conversacion_id)
        return [
            {
                "role": "user" if m.rol == "usuario" else "assistant",
                "content": m.contenido
            }
            for m in mensajes
        ]
