from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.hybrid import hybrid_property
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import Column, Integer, String, DateTime, Boolean
# from sqlalchemy.sql.sqltypes import String as SqlString
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
from passlib.context import CryptContext
from jose import JWTError, jwt
from .base_model import OrmBase
import datetime

# Set up ORM

class User(OrmBase): 
   __tablename__ = "users"

   id: Mapped[int] = mapped_column(primary_key=True)
   username: Mapped[str] = mapped_column(String(30), unique=True, index=True)
   last_name: Mapped[str] = mapped_column(String(30))
   first_name: Mapped[str] = mapped_column(String(30))
   email: Mapped[str] = mapped_column(String(30), unique=True, index=True)
   hashed_password: Mapped[str] = mapped_column(String(250))
   email_verified_at: Mapped[datetime.datetime] = mapped_column(DateTime)
   is_two_factor_auth_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
   active: Mapped[bool] = mapped_column(Boolean, default=False)
   has_verified_email: Mapped[bool] = mapped_column(Boolean, default=False)
   created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

   @hybrid_property
   def full_name(self):
      return f"{self.last_name}', '{self.first_name}"

   @full_name.setter
   def full_name(self, value):
      parts = value.split(' ')
      self.first_name = parts[0]
      self.last_name = parts[-1]
   

   def __repr__(self) -> str:
      return f"User(id={self.id!r}, name={self.last_name!r}', '{self.first_name!r}"
