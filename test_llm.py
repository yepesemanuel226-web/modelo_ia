"""
test_llm.py — Prueba el modelo LLaMA directamente con Groq.
Ejecutar: python test_llm.py
No necesita que la API esté corriendo.
"""
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

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
historial = []

print("=" * 50)
print("  Centro Médico Virtual — Asistente IA")
print("  Modelo: LLaMA 3.1 8B via Groq")
print("  Escribe 'salir' para terminar")
print("=" * 50)

while True:
    mensaje = input("\nTú: ").strip()

    if mensaje.lower() in ["salir", "exit", "quit"]:
        print("Cerrando sesión. ¡Hasta pronto!")
        break

    if not mensaje:
        continue

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
        print(f"\nAsistente: {respuesta}")

    except Exception as e:
        print(f"\n[Error]: {e}")