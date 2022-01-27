from app.extensions import request, MethodView, bcrypt, mail, \
    Message, render_template, create_access_token, jwt_required
from app.employee.models import Employee
from app.sensive import Sensive

# /employee
class EmployeeMethods(MethodView):

    # Cadastra novo funcionario
    def post(self):
        body = request.json

        name = body.get("name")
        birthdate = body.get("birthdate")
        cpf = body.get("cpf")
        phone_number = body.get("phone_number")
        email = body.get("email")
        password = body.get("password")

        # Verifica se dado e do tipo esperado, caso seja retorna erro
        if not isinstance(name, str) or not isinstance(birthdate, str) or not isinstance(cpf, str) or not \
            isinstance(phone_number, str) or not isinstance(email, str) or not isinstance(password, str):
            return {"code_status":"invalid data"}, 400
        
        # Verifica se CPF tem tamanho valido
        elif len(str(cpf)) != 11:
            return {"code_status":"invalid cpf format"}, 400

        # Verifica se cliente ja cadastrado
        employee_cpf = Employee.query.filter_by(cpf=cpf).first()
        employee_email = Employee.query.filter_by(email=email).first()
        if employee_cpf or employee_email:
            return {"code_status":"costumer already exists"}

        # Criptografa senha
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        # Salva funcionario no banco de dados, manda email e retorna sucesso
        employee = Employee(name=name, birthdate=birthdate, cpf=cpf, phone_number=phone_number, email=email, password_hash=password_hash)
        employee.save()

        msg = Message(
            sender=Sensive.EMAIL,
            recipients=[email],
            subject="Bem-vindo(a) a nossa academia!",
            html=render_template("email_employee.html", name=name)
        )
        mail.send(msg)

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
    decorators = [jwt_required()]
    # Retorna info do banco de dados de id especifico
    def get(self, id):
        employee = Employee.query.get_or_404(id)
        return employee.json()


    # Altera informacoes do funcionario
    def patch(self, id):
        body = request.json

        employee = Employee.query.get_or_404(id)

        name = body.get("name", employee.name)
        birthdate = body.get("birthdate", employee.birthdate)
        cpf = body.get("cpf", employee.cpf)
        phone_number = body.get("phone_number", employee.phone_number)

        # Verifica se dado e do tipo esperado, caso seja retorna erro
        if not isinstance(name, str) or not isinstance(birthdate, str) or not isinstance(cpf, str) or not isinstance(phone_number, str):
            return {"code_status":"invalid data"}, 400
        
        employee.name = name
        employee.birthdate = birthdate
        employee.cpf = cpf
        employee.phone_number = phone_number
        employee.update()

        return employee.json(), 200

    
    # Deleta cliente
    def delete(self, id):
        employee = Employee.query.get_or_404(id)
        employee.delete(employee)

        return {"code_status":"deleted"}, 200



# /employee/login
class EmployeeLogin(MethodView):
    def post(self):
        body = request.json

        email = body.get("email")
        password = body.get("password")

        # Verifica se dado e do tipo esperado, caso seja retorna erro
        if not isinstance(email, str) or not isinstance(password, str):
            return {"code_status":"invalid data"}, 400
        
        employee = Employee.query.filter_by(email=email).first()

        # Verifica se funcionario existe e se senha correta
        if not employee or not bcrypt.checkpw(password.encode(), employee.password_hash):
            return {"code_status":"invalid user or password"}, 400
        
        # Cria token do funcionario
        token = create_access_token(identity=employee.id)

        return {"token": token}, 200

