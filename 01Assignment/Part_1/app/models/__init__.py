print("Initializing package from assigment 1 models...")

VERSION = '1.0'

from .base_model import OrmBase
from .employee_model import Employee, Gender, Department, Role

__all__ = ["OrmBase", "get_session", "db_manager", "Employee", VERSION]
