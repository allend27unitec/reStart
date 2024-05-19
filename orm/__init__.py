"""
Data structures, used in project.

Add your new models here so Alembic could pick them up.

You may do changes in tables, then execute
`alembic revision --message="Your text" --autogenerate`
and alembic would generate new migration for you
in alembic/versions folder.
"""
print("Initializing package from orm...")

from .base_model import OrmBase
from .session_manager import db_manager
from .user_model import User

__all__ = ["OrmBase", "get_session", "db_manager", "User"]
