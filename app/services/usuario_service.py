from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCrear
from uuid import UUID


class UsuarioService:
    """Gestión de usuarios (pacientes y médicos)."""

    def __init__(self, db: Session):
        self.db = db

    def crear(self, datos: UsuarioCrear) -> Usuario:
        if datos.email:
            existente = self.buscar_por_email(datos.email)
            if existente:
                return existente

        usuario = Usuario(
            nombre=datos.nombre,
            email=datos.email,
            rol=datos.rol
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def obtener_por_id(self, usuario_id: UUID) -> Usuario:
        usuario = self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario

    def obtener_todos(self) -> list[Usuario]:
        return self.db.query(Usuario).filter(Usuario.activo == True).all()

    def buscar_por_email(self, email: str) -> Usuario:
        return self.db.query(Usuario).filter(Usuario.email == email).first()
