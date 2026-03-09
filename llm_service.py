from sqlalchemy.orm import Session
from groq import Groq
from app.config import GROQ_API_KEY
from app.services.mensaje_service import MensajeService
from uuid import UUID

SYSTEM_PROMPT = """
Eres un asistente médico inteligente del Centro Médico Virtual.
Tu función es orientar a los pacientes con posibles diagnósticos preliminares
y apoyar a los médicos con información clínica relevante.

Reglas que debes seguir siempre:
- Responde siempre en español, con lenguaje claro y empático.
- Nunca reemplaces la consulta médica presencial; siempre recomienda acudir a un médico.
- Ante síntomas de emergencia (dolor en el pecho, dificultad respiratoria grave,
  pérdida de consciencia), indica de inmediato que llame al servicio de emergencias.
- Puedes preguntar al paciente sobre síntomas, duración, intensidad y antecedentes
  médicos para dar una orientación más precisa.
- No prescribas medicamentos con dosis específicas.
- Mantén el contexto de la conversación para dar respuestas coherentes.
- Si el usuario indica que es médico, puedes usar terminología clínica más técnica.
"""


class LLMService:
    """
    Servicio de IA generativa usando Groq + LLaMA 3.1-8b-instant.
    Gestiona el historial de conversación y genera respuestas médicas.
    """

    def __init__(self, db: Session):
        self.db = db
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY no está configurada en las variables de entorno")
        self.client = Groq(api_key=GROQ_API_KEY)
        self.mensaje_service = MensajeService(db)

    def generar_respuesta(self, conversacion_id: UUID, mensaje_usuario: str) -> str:
        """
        Genera una respuesta del LLM dado el mensaje del usuario
        y el historial completo de la conversación almacenado en BD.
        """
        historial = self.mensaje_service.obtener_historial_como_dict(conversacion_id)
        historial.append({"role": "user", "content": mensaje_usuario})

        try:
            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *historial
                ],
                max_tokens=600,
                temperature=0.7,
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            return f"Lo siento, en este momento no puedo procesar tu consulta. Error: {str(e)}"
