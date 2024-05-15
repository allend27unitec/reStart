
class Commission:
   def __init__(self):
      print("Commission initiated")

   def calculate_commission(self, sales: int) -> float:
      return sales * .05

commission = Commission()
