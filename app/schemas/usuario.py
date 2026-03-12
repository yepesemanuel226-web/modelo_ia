from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class UsuarioCrear(BaseModel):
    nombre:   str            = Field(..., min_length=2, max_length=100, example="Ana Torres")
    email:    Optional[EmailStr] = Field(None, example="ana@email.com")
    rol:      str            = Field(default="paciente", example="paciente")
    username: Optional[str]  = Field(None, example="ana123")
    password: Optional[str]  = Field(None, example="1234")


class UsuarioRespuesta(BaseModel):
    id:             UUID
    nombre:         str
    email:          Optional[str]
    rol:            str
    activo:         bool
    fecha_registro: Optional[datetime]
    username:       Optional[str]

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str