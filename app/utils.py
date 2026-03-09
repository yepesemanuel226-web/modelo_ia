"""
Helper para manejar UUID de forma compatible
entre SQLite (pruebas locales) y PostgreSQL (Supabase/Render).
"""
import uuid
from sqlalchemy import String
from app.config import DATABASE_URL


def uuid_column(primary_key=False):
    """Retorna una columna UUID compatible con el motor actual."""
    if DATABASE_URL.startswith("sqlite"):
        from sqlalchemy import Column
        return Column(String(36), primary_key=primary_key, default=lambda: str(uuid.uuid4()))
    else:
        from sqlalchemy import Column
        from sqlalchemy.dialects.postgresql import UUID
        return Column(UUID(as_uuid=True), primary_key=primary_key, default=uuid.uuid4)