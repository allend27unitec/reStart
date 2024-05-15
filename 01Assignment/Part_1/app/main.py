import sys
sys.path.append("../../../")
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
    scoped_session
)
from passlib.context import CryptContext
from jose import JWTError, jwt
from project.settings import settings
from orm.employee_model import Employee
from orm.base_model import OrmBase
from classes.Commission import commission
from classes.Contract import contract
from classes.ContractCommission import contract_commission
from classes.SalariedContract import salaried_contract
from classes.HourlyContract import hourly_contract
from classes.FreelancerContract import freelancer_contract

# Set up database connection
def create_session():
    try:
        engine = settings.postgresql_engine()
        session_factory = sessionmaker(bind=engine)
        print(f"Postgresql Connection successful")
        return scoped_session(session_factory)
    except Exception as e:
         print(f"Postgresql Connection Exception {e}")

if __name__ == '__main__':
#    Session = create_session()
    print("Commission: ", commission.calculate_commission(23000))
