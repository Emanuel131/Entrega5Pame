from app.extensions import Blueprint
from app.employee.controller import EmployeeMethods, EmployeeMethodsId

employee_api = Blueprint("employee_api", __name__)

employee_api.add_url_rule("/employee", view_func = EmployeeMethods.as_view('geralFuncionario'), methods=['GET', 'POST'])
employee_api.add_url_rule("/employee/<int:id>", view_func = EmployeeMethodsId.as_view('geralFuncionarioId'), methods=['GET', 'PATCH', 'DELETE'])
