from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.diagnostico import Diagnostico
from app.schemas.nuevos_schemas import DiagnosticoCrear, DiagnosticoRespuesta

router = APIRouter(prefix="/diagnosticos", tags=["Diagnósticos"])


@router.post("/", response_model=DiagnosticoRespuesta, status_code=201)
def crear_diagnostico(data: DiagnosticoCrear, db: Session = Depends(get_db)):
    diag = Diagnostico(**data.model_dump())
    db.add(diag)
    db.commit()
    db.refresh(diag)
    return diag


@router.get("/usuario/{usuario_id}", response_model=list[DiagnosticoRespuesta])
def diagnosticos_por_usuario(usuario_id: str, db: Session = Depends(get_db)):
    return db.query(Diagnostico).filter(
        Diagnostico.usuario_id == usuario_id
    ).order_by(Diagnostico.created_at.desc()).all()


@router.get("/conversacion/{conversacion_id}", response_model=list[DiagnosticoRespuesta])
def diagnosticos_por_conversacion(conversacion_id: str, db: Session = Depends(get_db)):
    return db.query(Diagnostico).filter(
        Diagnostico.conversacion_id == conversacion_id
    ).order_by(Diagnostico.created_at.desc()).all()


@router.get("/{diagnostico_id}", response_model=DiagnosticoRespuesta)
def obtener_diagnostico(diagnostico_id: str, db: Session = Depends(get_db)):
    d = db.query(Diagnostico).filter(Diagnostico.id == diagnostico_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Diagnóstico no encontrado")
    return d
