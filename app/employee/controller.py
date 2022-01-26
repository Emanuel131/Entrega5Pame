from app.employee.models import Employee
from app.extensions import request, MethodView

# /employee
class EmployeeMethods(MethodView):

    # Insere info no banco de dados
    def post(self):
        body = request.json

        name = body.get("name")
        birthdate = body.get("birthdate")
        cpf = body.get("cpf")
        phone_number = body.get("phone_number")

        # Verifica se dado e do tipo esperado, caso seja retorna erro
        if not isinstance(name, str) or not isinstance(birthdate, str) or not isinstance(cpf, int) or not isinstance(phone_number, str):
            return {"code_status":"invalid data"}, 400
        
        # Verifica se CPF tem tamanho valido
        elif cpf < 11:
            return {"code_status":"invalid data"}, 400

        # Verifica se cliente ja cadastrado
        employee = Employee.query.filter_by(cpf=cpf).first()
        if employee:
            return {"code_status":"employee already exists"}

        # Caso nao seja, salva no banco de dados e retorna sucesso
        employee = Employee(name=name, birthdate=birthdate, cpf=cpf, phone_number=phone_number)
        employee.save()
        return employee.json(), 200


    # Retorna info do banco de dados
    def get(self):
        employees = Employee.query.all()
        body = {}

        for employee in employees:
            body[employee.id] = employee.json()
        
        return body



# /employee/<int:id>
class EmployeeMethodsId(MethodView):

    # Retorna info do banco de dados de id especifico
    def get(self, id):
        employee = Employee.query.get_or_404(id)
        return employee.json()


    # Altera informacoes do funcionario
    def patch(self, id):
        body = request.json

        employee = Employee.query.get_or_404(id)

        name = body.get("name")
        birthdate = body.get("birthdate")
        cpf = body.get("cpf")
        phone_number = body.get("phone_number")

        # Verifica se dado e do tipo esperado, caso seja retorna erro
        if not isinstance(name, str) or not isinstance(birthdate, str) or not isinstance(cpf, int) or not isinstance(phone_number, str):
            return {"code_status":"invalid data"}, 400
        
        employee.name = name
        employee.birthdate = birthdate
        employee.cpf = cpf
        employee.phone_number = phone_number

        return employee.json(), 200

    
    # Deleta cliente
    def delete(self, id):
        employee = Employee.query.get_or_404(id)
        employee.delete(employee)

        return {"code_status":"deleted"}, 200

