# Write a Python class Employee with attributes like emp_id, emp_name, emp_salary, and emp_department and methods like calculate_emp_salary, emp_assign_department, and print_employee_details.
# - Raise a custom exception when the salary is lower than 40,000 which is lower than the minimum wage
# - Use 'assign_department' method to change the department of an employee.
# - Use 'print_employee_details' method to print the details of an employee.
# - Use 'calculate_emp_salary' method takes two arguments: salary and hours_worked,
# which is the number of hours worked by the employee. If the number of hours worked is more than 50,
# the method computes overtime and adds it to the salary. Overtime is calculated as following formula:
#
# ```
# overtime = hours_worked – 50
# overtime amount = (overtime * (salary / 50))
# ```
#
# ```
# Sample Employee Data:
# "ADAMS", "E7876", 50000, "ACCOUNTING"
# "JONES", "E7499", 45000, "RESEARCH"
# "MARTIN", "E7900", 50000, "SALES"
# "SMITH", "E7698", 55000, "OPERATIONS"
# "KING", "E5698", 20000, "RESEARCH"
# ```
class Employee:
    def __init__(self, name, emp_id, salary, department):
        # ========================================================================
        #                 _                                _
        #                | |                              | |
        #    ___ ___   __| | ___    __ _  ___   ___  ___  | |__   ___ _ __ ___
        #   / __/ _ \ / _` |/ _ \  / _` |/ _ \ / _ \/ __| | '_ \ / _ \ '__/ _ \
        #  | (_| (_) | (_| |  __/ | (_| | (_) |  __/\__ \ | | | |  __/ | |  __/
        #   \___\___/ \__,_|\___|  \__, |\___/ \___||___/ |_| |_|\___|_|  \___|
        #                           __/ |
        #                          |___/
        # ========================================================================
        pass

    def calculate_salary(self, base_salary, hours_worked):
        # ========================================================================
        #                 _                                _
        #                | |                              | |
        #    ___ ___   __| | ___    __ _  ___   ___  ___  | |__   ___ _ __ ___
        #   / __/ _ \ / _` |/ _ \  / _` |/ _ \ / _ \/ __| | '_ \ / _ \ '__/ _ \
        #  | (_| (_) | (_| |  __/ | (_| | (_) |  __/\__ \ | | | |  __/ | |  __/
        #   \___\___/ \__,_|\___|  \__, |\___/ \___||___/ |_| |_|\___|_|  \___|
        #                           __/ |
        #                          |___/
        # ========================================================================
        pass

    def assign_department(self, emp_department):
        # ========================================================================
        #                 _                                _
        #                | |                              | |
        #    ___ ___   __| | ___    __ _  ___   ___  ___  | |__   ___ _ __ ___
        #   / __/ _ \ / _` |/ _ \  / _` |/ _ \ / _ \/ __| | '_ \ / _ \ '__/ _ \
        #  | (_| (_) | (_| |  __/ | (_| | (_) |  __/\__ \ | | | |  __/ | |  __/
        #   \___\___/ \__,_|\___|  \__, |\___/ \___||___/ |_| |_|\___|_|  \___|
        #                           __/ |
        #                          |___/
        # ========================================================================
        pass

    def print_employee_details(self):
        # ========================================================================
        #                 _                                _
        #                | |                              | |
        #    ___ ___   __| | ___    __ _  ___   ___  ___  | |__   ___ _ __ ___
        #   / __/ _ \ / _` |/ _ \  / _` |/ _ \ / _ \/ __| | '_ \ / _ \ '__/ _ \
        #  | (_| (_) | (_| |  __/ | (_| | (_) |  __/\__ \ | | | |  __/ | |  __/
        #   \___\___/ \__,_|\___|  \__, |\___/ \___||___/ |_| |_|\___|_|  \___|
        #                           __/ |
        #                          |___/
        # ========================================================================
        pass


# Sample output
# ------------------------------------------------
# Original Employee Details:
#
# Name:  ADAMS
# ID:  E7876
# Salary:  50000
# Department:  ACCOUNTING
# ----------------------
#
# Name:  JONES
# ID:  E7499
# Salary:  45000
# Department:  RESEARCH
# ----------------------
#
# Name:  MARTIN
# ID:  E7900
# Salary:  50000
# Department:  SALES
# ----------------------
#
# Name:  SMITH
# ID:  E7698
# Salary:  55000
# Department:  OPERATIONS
# ------------------------------------------------
# Updated Employee Details:
#
# Name:  ADAMS
# ID:  E7876
# Salary:  50000
# Department:  OPERATIONS
# ----------------------
#
# Name:  JONES
# ID:  E7499
# Salary:  46800.0
# Department:  RESEARCH
# ----------------------
#
# Name:  MARTIN
# ID:  E7900
# Salary:  50000
# Department:  SALES
# ----------------------
#
# Name:  SMITH
# ID:  E7698
# Salary:  66000.0
# Department:  SALES
# ------------------------------------------------
def main():
    employee1 = Employee("ADAMS", "E7876", 50000, "ACCOUNTING")
    employee2 = Employee("JONES", "E7499", 45000, "RESEARCH")
    employee3 = Employee("MARTIN", "E7900", 50000, "SALES")
    employee4 = Employee("SMITH", "E7698", 55000, "OPERATIONS")

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

    employee5 = Employee("KING", "E5698", 20000, "RESEARCH")


if __name__ == "__main__":
    main()
