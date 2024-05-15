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

db:
    employee1 = Employee("ADAMS", "E7876", 50000, "ACCOUNTING")
    employee2 = Employee("JONES", "E7499", 45000, "RESEARCH")
    employee3 = Employee("MARTIN", "E7900", 50000, "SALES")
    employee4 = Employee("SMITH", "E7698", 55000, "OPERATIONS")
    employee5 = Employee("KING", "E5698", 20000, "RESEARCH")

    print("Original Employee Details:")
    employee1.print_employee_details()
    employee2.print_employee_details()
    employee3.print_employee_details()
    employee4.print_employee_details()

    # Change the departments of employee1 and employee4
    employee1.assign_department("OPERATIONS")
    employee4.assign_department("SALES")

    # Now calculate the overtime of the employees who are eligible:
    employee2.calculate_salary(45000, 52)
    employee4.calculate_salary(45000, 60)

    print("Updated Employee Details:")
    employee1.print_employee_details()
    employee2.print_employee_details()
    employee3.print_employee_details()
    employee4.print_employee_details()


if __name__ == '__main__':
#    Session = create_session()
    print("Commission: ", commission.calculate_commission(23000))
