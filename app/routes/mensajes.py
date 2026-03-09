from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.schemas import MensajeRespuesta, ChatRequest, ChatResponse
from app.services import ConversacionService, MensajeService, LLMService

router = APIRouter(prefix="/mensajes", tags=["Mensajes / Chat"])


@router.post("/chat", response_model=ChatResponse)
def chat_medico(datos: ChatRequest, db: Session = Depends(get_db)):
    """
    Endpoint principal del asistente médico IA.

    Flujo:
    1. Busca la conversación activa del usuario o crea una nueva.
    2. Guarda el mensaje del usuario en BD.
    3. Recupera el historial completo y llama al LLM (Groq/LLaMA).
    4. Guarda la respuesta del asistente en BD.
    5. Retorna la respuesta al cliente.
    """
    conv_service = ConversacionService(db)
    msg_service  = MensajeService(db)
    llm_service  = LLMService(db)

    # 1. Conversación activa o nueva
    conversacion = conv_service.obtener_activa_por_usuario(datos.usuario_id)
    if not conversacion:
        conversacion = conv_service.crear(datos.usuario_id)

    # 2. Guardar mensaje del usuario
    msg_service.guardar(
        conversacion_id=conversacion.id,
        rol="usuario",
        contenido=datos.mensaje
    )

    # 3. Generar respuesta con el LLM
    respuesta_ia = llm_service.generar_respuesta(
        conversacion_id=conversacion.id,
        mensaje_usuario=datos.mensaje
    )

    # 4. Guardar respuesta del asistente
    msg_service.guardar(
        conversacion_id=conversacion.id,
        rol="asistente",
        contenido=respuesta_ia
    )

    return ChatResponse(
        conversacion_id=conversacion.id,
        respuesta=respuesta_ia
    )


@router.get("/historial/{conversacion_id}", response_model=list[MensajeRespuesta])
def historial_mensajes(conversacion_id: UUID, db: Session = Depends(get_db)):
    """Retorna todos los mensajes de una conversación."""
    return MensajeService(db).obtener_historial(conversacion_id)
