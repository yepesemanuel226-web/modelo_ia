from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.schemas import UsuarioCrear, UsuarioRespuesta
from app.schemas.usuario import LoginRequest
from app.services import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/registro", response_model=UsuarioRespuesta, status_code=201)
def registrar_usuario(datos: UsuarioCrear, db: Session = Depends(get_db)):
    """Registra un nuevo usuario con username y password."""
    return UsuarioService(db).crear(datos)


@router.post("/login", response_model=UsuarioRespuesta)
def login_usuario(datos: LoginRequest, db: Session = Depends(get_db)):
    """Autentica un usuario con username y password."""
    return UsuarioService(db).login(datos.username, datos.password)


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