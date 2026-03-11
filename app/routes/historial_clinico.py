from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.historial_clinico import HistorialClinico
from app.schemas.nuevos_schemas import HistorialClinicoCrear, HistorialClinicoRespuesta
from typing import List

router = APIRouter(prefix="/historial-clinico", tags=["Historial Clínico"])


@router.post("/", response_model=HistorialClinicoRespuesta, status_code=201)
def crear_historial(data: HistorialClinicoCrear, db: Session = Depends(get_db)):
    h = HistorialClinico(**data.model_dump())
    db.add(h)
    db.commit()
    db.refresh(h)
    return h


@router.get("/usuario/{usuario_id}", response_model=List[HistorialClinicoRespuesta])
def historial_por_usuario(usuario_id: str, db: Session = Depends(get_db)):
    return db.query(HistorialClinico).filter(
        HistorialClinico.usuario_id == usuario_id
    ).order_by(HistorialClinico.fecha.desc()).all()


@router.get("/{historial_id}", response_model=HistorialClinicoRespuesta)
def obtener_historial(historial_id: str, db: Session = Depends(get_db)):
    h = db.query(HistorialClinico).filter(HistorialClinico.id == historial_id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    return h