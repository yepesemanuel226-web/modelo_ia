"""
test_api.py — Prueba los endpoints de la API completa.
Requiere que la API esté corriendo: uvicorn main:api --reload
Ejecutar en otra terminal: python test_api.py
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def separador(titulo):
    print(f"\n{'=' * 50}")
    print(f"  {titulo}")
    print("=" * 50)


# ── 1. Health check ──────────────────────────────────
separador("1. Health Check")
r = requests.get(f"{BASE_URL}/")
print(r.json())


# ── 2. Crear usuario paciente ─────────────────────────
separador("2. Crear usuario paciente")
r = requests.post(f"{BASE_URL}/usuarios/", json={
    "nombre": "Carlos Pérez",
    "email": "carlos@email.com",
    "rol": "paciente"
})
usuario = r.json()
print(json.dumps(usuario, indent=2, default=str))
usuario_id = usuario["id"]


# ── 3. Enviar mensaje al chat IA ──────────────────────
separador("3. Chat con asistente médico IA")
r = requests.post(f"{BASE_URL}/mensajes/chat", json={
    "usuario_id": usuario_id,
    "mensaje": "Tengo dolor de cabeza fuerte desde hace 2 días y fiebre de 38°C"
})
chat = r.json()
print(f"\nRespuesta IA:\n{chat['respuesta']}")
conversacion_id = chat["conversacion_id"]


# ── 4. Continuar la conversación ──────────────────────
separador("4. Continuar conversación (con contexto)")
r = requests.post(f"{BASE_URL}/mensajes/chat", json={
    "usuario_id": usuario_id,
    "mensaje": "El dolor es pulsante y empeora con la luz"
})
print(f"\nRespuesta IA:\n{r.json()['respuesta']}")


# ── 5. Ver historial ──────────────────────────────────
separador("5. Historial de la conversación")
r = requests.get(f"{BASE_URL}/mensajes/historial/{conversacion_id}")
mensajes = r.json()
for m in mensajes:
    print(f"\n[{m['rol'].upper()}]: {m['contenido'][:100]}...")


# ── 6. Ver conversaciones del usuario ─────────────────
separador("6. Conversaciones del usuario")
r = requests.get(f"{BASE_URL}/conversaciones/usuario/{usuario_id}")
print(json.dumps(r.json(), indent=2, default=str))


print("\n✅ Todas las pruebas completadas")