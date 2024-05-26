
class Commission:
   def __init__(self):
      print("Commission initiated")

   def calculate_commission(self, sales: int) -> str:
      if sales > 8000:
         c = sales * .08
      elif sales > 6000:
         c = sales * .05
      else:
         c = sales * .04

      return ("{:.2f}".format(c))

commission = Commission()
