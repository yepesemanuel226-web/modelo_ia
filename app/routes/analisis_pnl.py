from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.analisis_pnl import AnalisisPNL
from app.schemas.nuevos_schemas import AnalisisPNLCrear, AnalisisPNLRespuesta
from app.services.pnl_service import analizar_texto
from typing import List

router = APIRouter(prefix="/analisis-pnl", tags=["Análisis PNL"])


@router.post("/", response_model=AnalisisPNLRespuesta, status_code=201)
def crear_analisis(data: AnalisisPNLCrear, db: Session = Depends(get_db)):
    resultado = analizar_texto(data.texto_original)
    analisis = AnalisisPNL(
        conversacion_id=data.conversacion_id,
        historial_id=data.historial_id,
        texto_original=data.texto_original,
        resumen=resultado["resumen"],
        entidades=resultado["entidades"],
        traduccion=resultado["traduccion"],
        sentimiento=resultado["sentimiento"],
        score_sentimiento=resultado["score_sentimiento"]
    )
    db.add(analisis)
    db.commit()
    db.refresh(analisis)
    return analisis


@router.get("/conversacion/{conversacion_id}", response_model=List[AnalisisPNLRespuesta])
def analisis_por_conversacion(conversacion_id: str, db: Session = Depends(get_db)):
    return db.query(AnalisisPNL).filter(
        AnalisisPNL.conversacion_id == conversacion_id
    ).order_by(AnalisisPNL.created_at.desc()).all()


@router.get("/{analisis_id}", response_model=AnalisisPNLRespuesta)
def obtener_analisis(analisis_id: str, db: Session = Depends(get_db)):
    a = db.query(AnalisisPNL).filter(AnalisisPNL.id == analisis_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Análisis no encontrado")
    return a