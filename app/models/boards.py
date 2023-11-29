from sqlalchemy import Column, DateTime, Integer, Table, Text, func

from app.models.database import metadata

boards = Table(
    "boards",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text, nullable=False),
    Column(
        "created_at",
        DateTime,
        server_default=func.current_timestamp(),
        nullable=False,
    ),
    Column(
        "updated_at",
        DateTime,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    ),
)
