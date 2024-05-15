"""
Data structures, used in project.

Add your new models here so Alembic could pick them up.

You may do changes in tables, then execute
`alembic revision --message="Your text" --autogenerate`
and alembic would generate new migration for you
in alembic/versions folder.
"""
print("Initializing package from assigment 1 ORM...")

VERSION = '1.0'

from .base_model import OrmBase
# from .session_manager import db_manager
from .employee_model import Employee

__all__ = ["OrmBase", "get_session", "db_manager", "Employee", VERSION]
