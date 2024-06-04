from uuid import UUID, uuid4
from pydantic import Json
from sqlalchemy import BigInteger, String, JSON, DateTime
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    mapped_column
)
from .base_model import OrmBase
from datetime import datetime

# Set up ORM

Base = declarative_base()

class Employee(OrmBase): 
    __tablename__ = "employee"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    emp_number: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    last_name: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(255))
    middle_name: Mapped[str] = mapped_column(String(255), nullable=True)
    salary: Mapped[int] = mapped_column(BigInteger, nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=True)
    contract_type: Mapped[str] = mapped_column(JSON, nullable=True) # the type of contract
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
