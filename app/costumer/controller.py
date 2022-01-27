from click import decorators
from app.extensions import request, MethodView, Message, render_template, \
    mail, bcrypt, jwt, create_access_token, jwt_required
from app.costumer.models import Costumer
from app.sensive import Sensive

# /costumer
class CostumerMethods(MethodView):

    # Cadastra novo cliente
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
        if len(str(cpf)) != 11:
            return {"code_status":"invalid cpf format"}, 400

        # Verifica se cliente ja cadastrado
        costumer_cpf = Costumer.query.filter_by(cpf=cpf).first()
        costumer_email = Costumer.query.filter_by(email=email).first()
        if costumer_cpf or costumer_email:
            return {"code_status":"costumer already exists"}

        # Criptografa senha
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        # Salva cliente no banco de dados, manda email e retorna sucesso
        costumer = Costumer(name=name, birthdate=birthdate, cpf=cpf, phone_number=phone_number, email=email, password_hash=password_hash)
        costumer.save()

        msg = Message(
            sender=Sensive.EMAIL,
            recipients=[email],
            subject="Bem-vindo(a) a nossa academia!",
            html=render_template("email_costumer.html", name=name)
        )
        mail.send(msg)

        return costumer.json(), 200


    # Retorna info do banco de dados
    def get(self):
        costumers = Costumer.query.all()
        body = {}

        for costumer in costumers:
            body[costumer.id] = costumer.json()
        
        return body



# /costumer/<int:id>
class CostumerMethodsId(MethodView):
    decorators = [jwt_required()]
    # Retorna info do banco de dados de id especifico
    def get(self, id):
        costumer = Costumer.query.get_or_404(id)
        return costumer.json()


    # Altera informacoes do cliente
    def patch(self, id):
        body = request.json

        costumer = Costumer.query.get_or_404(id)

        name = body.get("name", costumer.name)
        birthdate = body.get("birthdate", costumer.birthdate)
        cpf = body.get("cpf", costumer.cpf)
        phone_number = body.get("phone_number", costumer.phone_number)

        # Verifica se dado e do tipo esperado, caso seja retorna erro
        if not isinstance(name, str) or not isinstance(birthdate, str) or not isinstance(cpf, str) or not isinstance(phone_number, str):
            return {"code_status":"invalid data"}, 400
        
        costumer.name = name
        costumer.birthdate = birthdate
        costumer.cpf = cpf
        costumer.phone_number = phone_number
        costumer.update()

        return costumer.json(), 200

    
    # Deleta cliente
    def delete(self, id):
        costumer = Costumer.query.get_or_404(id)
        costumer.delete(costumer)

        return {"code_status":"deleted"}, 200


# Cliente marcar horario
# /costumer/schedule/<int:id>
class CostumerMethodsScheduleId(MethodView):
    decorators = [jwt_required()]
    # Altera informacoes do cliente
    def patch(self, id):
        body = request.json

        costumer = Costumer.query.get_or_404(id)

        init_time_scheduled = body.get("init_time_scheduled", costumer.init_time_scheduled)
        final_time_scheduled = body.get("final_time_scheduled", costumer.final_time_scheduled)

        # Verifica se dado e do tipo esperado, caso seja retorna erro
        if not isinstance(init_time_scheduled, str) or not isinstance(final_time_scheduled, str):
            return {"code_status":"invalid data"}, 400
        
        costumer.init_time_scheduled = init_time_scheduled
        costumer.final_time_scheduled = final_time_scheduled
        costumer.update()

        return costumer.json(), 200


# /costumer/login
class CostumerLogin(MethodView):
    
    def post(self):
        body = request.json

        email = body.get("email")
        password = body.get("password")

        # Verifica se dado e do tipo esperado, caso seja retorna erro
        if not isinstance(email, str) or not isinstance(password, str):
            return {"code_status":"invalid data"}, 400
        
        costumer = Costumer.query.filter_by(email=email).first()

        # Verifica se cliente existe e se senha correta
        if not costumer or not bcrypt.checkpw(password.encode(), costumer.password_hash):
            return {"code_status":"invalid user or password"}, 400
        
        # Cria token do cliente
        token = create_access_token(identity=costumer.id)

        return {"token": token}, 200

