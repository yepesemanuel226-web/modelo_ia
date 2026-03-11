from dotenv import load_dotenv
load_dotenv()

from app.database import Base, engine
from app.models.usuario import Usuario
from app.models.conversacion import Conversacion
from app.models.mensaje import Mensaje
from app.models.historial_clinico import HistorialClinico
from app.models.historial_paciente import HistorialPaciente
from app.models.diagnostico import Diagnostico
from app.models.analisis_pnl import AnalisisPNL
from app.models.cita import Cita

Base.metadata.create_all(bind=engine)