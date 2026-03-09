from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.schemas import UsuarioCrear, UsuarioRespuesta
from app.services import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=UsuarioRespuesta, status_code=201)
def crear_usuario(datos: UsuarioCrear, db: Session = Depends(get_db)):
    """Registra un nuevo usuario (paciente o médico)."""
    return UsuarioService(db).crear(datos)


@router.get("/", response_model=list[UsuarioRespuesta])
def listar_usuarios(db: Session = Depends(get_db)):
    """Lista todos los usuarios activos."""
    return UsuarioService(db).obtener_todos()


@router.get("/{usuario_id}", response_model=UsuarioRespuesta)
def obtener_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    """Obtiene un usuario por su UUID."""
    return UsuarioService(db).obtener_por_id(usuario_id)
