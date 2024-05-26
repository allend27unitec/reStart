print("Initializing package from assigment 1 part 3 models...")

VERSION = '1.0'

from .base_model import OrmBase
from .owner_model import Owner, OwnsCar
from .car_model import Car


__all__ = ["OrmBase", "Owner", "OwnsCar", "Car", 'VERSION']
