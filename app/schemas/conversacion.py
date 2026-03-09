from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class ConversacionRespuesta(BaseModel):
    id:         UUID
    usuario_id: UUID
    estado:     str
    inicio:     datetime
    fin:        Optional[datetime]

    class Config:
        from_attributes = True
