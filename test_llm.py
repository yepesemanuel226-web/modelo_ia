"""
test_llm.py — Prueba el modelo LLaMA directamente con Groq.
Guarda la conversación en la BD (Supabase o SQLite según .env).
Ejecutar: python test_llm.py
"""
from dotenv import load_dotenv
load_dotenv()

from groq import Groq
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Usuario, Conversacion, Mensaje
from app.models.usuario import Usuario
from app.models.conversacion import Conversacion
from app.models.mensaje import Mensaje
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SYSTEM_PROMPT = """
Eres un asistente médico inteligente del Centro Médico Virtual.
Tu función es orientar a los pacientes con posibles diagnósticos preliminares
y apoyar a los médicos con información clínica relevante.
Responde siempre en español, con lenguaje claro y empático.
Nunca reemplaces la consulta médica presencial.
Ante síntomas de emergencia indica que llame a emergencias de inmediato.
"""

client = Groq(api_key=GROQ_API_KEY)


def obtener_o_crear_usuario(db: Session, nombre: str = "Test Local") -> Usuario:
    usuario = db.query(Usuario).filter(Usuario.nombre == nombre).first()
    if not usuario:
        usuario = Usuario(nombre=nombre, email="test@local.com", rol="paciente")
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
    return usuario


def crear_conversacion(db: Session, usuario_id) -> Conversacion:
    conversacion = Conversacion(
        usuario_id=str(usuario_id),
        estado="activa"
    )
    db.add(conversacion)
    db.commit()
    db.refresh(conversacion)
    return conversacion


def guardar_mensaje(db: Session, conversacion_id, rol: str, contenido: str):
    mensaje = Mensaje(
        conversacion_id=str(conversacion_id),
        rol=rol,
        contenido=contenido
    )
    db.add(mensaje)
    db.commit()


def main():
    db = SessionLocal()
    historial = []

    print("=" * 50)
    print("  Centro Médico Virtual — Asistente IA")
    print("  Modelo: LLaMA 3.1 8B via Groq")
    print("  Conversación guardada en BD")
    print("  Escribe 'salir' para terminar")
    print("=" * 50)

    # Crear usuario y conversación de prueba
    usuario = obtener_o_crear_usuario(db)
    conversacion = crear_conversacion(db, usuario.id)
    print(f"\n[Sesión iniciada — conversacion_id: {conversacion.id}]\n")

    while True:
        mensaje = input("Tú: ").strip()

        if mensaje.lower() in ["salir", "exit", "quit"]:
            # Cerrar conversación
            conversacion.estado = "cerrada"
            db.commit()
            print(f"\n[Conversación guardada en BD con id: {conversacion.id}]")
            print("Cerrando sesión. ¡Hasta pronto!")
            break

        if not mensaje:
            continue

        # Guardar mensaje del usuario en BD
        guardar_mensaje(db, conversacion.id, "usuario", mensaje)
        historial.append({"role": "user", "content": mensaje})

        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *historial
                ],
                max_tokens=600,
                temperature=0.7,
            )
            respuesta = completion.choices[0].message.content.strip()
            historial.append({"role": "assistant", "content": respuesta})

            # Guardar respuesta del asistente en BD
            guardar_mensaje(db, conversacion.id, "asistente", respuesta)

            print(f"\nAsistente: {respuesta}\n")

        except Exception as e:
            print(f"\n[Error]: {e}")

    db.close()


if __name__ == "__main__":
    main()