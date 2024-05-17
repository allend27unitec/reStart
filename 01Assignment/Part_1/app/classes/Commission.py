import random
#from orm.employee_model import Employee, Gender, Role, Department
#from orm.base_model import OrmBase

class Commission:
   def __init__(self):
      print("Commission initiated")

   def calculate_commission(self, emp) -> float:
      return random.randrange(1000, 10000) * .05

commission = Commission()
