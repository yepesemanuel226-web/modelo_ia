from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.cita import Cita
from app.schemas.nuevos_schemas import CitaCrear, CitaActualizar, CitaRespuesta

router = APIRouter(prefix="/citas", tags=["Citas Médicas"])


@router.post("/", response_model=CitaRespuesta, status_code=201)
def crear_cita(data: CitaCrear, db: Session = Depends(get_db)):
    cita = Cita(**data.model_dump())
    db.add(cita)
    db.commit()
    db.refresh(cita)
    return cita


@router.get("/", response_model=list[CitaRespuesta])
def listar_citas(db: Session = Depends(get_db)):
    return db.query(Cita).order_by(Cita.fecha_cita).all()


@router.get("/paciente/{paciente_id}", response_model=list[CitaRespuesta])
def citas_por_paciente(paciente_id: str, db: Session = Depends(get_db)):
    return db.query(Cita).filter(Cita.paciente_id == paciente_id).order_by(Cita.fecha_cita).all()


@router.get("/medico/{medico_id}", response_model=list[CitaRespuesta])
def citas_por_medico(medico_id: str, db: Session = Depends(get_db)):
    return db.query(Cita).filter(Cita.medico_id == medico_id).order_by(Cita.fecha_cita).all()


@router.get("/{cita_id}", response_model=CitaRespuesta)
def obtener_cita(cita_id: str, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita


@router.patch("/{cita_id}", response_model=CitaRespuesta)
def actualizar_cita(cita_id: str, data: CitaActualizar, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    estados_validos = {"pendiente", "confirmada", "completada", "cancelada"}
    if data.estado and data.estado not in estados_validos:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Use: {estados_validos}")

    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(cita, campo, valor)

    db.commit()
    db.refresh(cita)
    return cita


@router.delete("/{cita_id}", status_code=204)
def eliminar_cita(cita_id: str, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    db.delete(cita)
    db.commit()
