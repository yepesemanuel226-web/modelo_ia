from dotenv import load_dotenv
load_dotenv()  # Cargar .env ANTES de cualquier otra importación

from app.database import Base, engine
from app.models.usuario import Usuario
from app.models.conversacion import Conversacion
from app.models.mensaje import Mensaje

# Crear tablas en SQLite si no existen
Base.metadata.create_all(bind=engine)