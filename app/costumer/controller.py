from app.costumer.models import Costumer
from app.extensions import request, MethodView

# /costumer
class CostumerMethods(MethodView):

    # Cadastra novo cliente
    def post(self):
        body = request.json

        name = body.get("name")
        birthdate = body.get("birthdate")
        cpf = body.get("cpf")
        phone_number = body.get("phone_number")

        # Verifica se dado e do tipo esperado, caso seja retorna erro
        if not isinstance(name, str) or not isinstance(birthdate, str) or not isinstance(cpf, str) or not isinstance(phone_number, str):
            return {"code_status":"invalid data"}, 400
        
        # Verifica se CPF tem tamanho valido
        if len(str(cpf)) != 11:
            return {"code_status":"invalid cpf format"}, 400

        # Verifica se cliente ja cadastrado
        costumer = Costumer.query.filter_by(cpf=cpf).first()
        if costumer:
            return {"code_status":"costumer already exists"}

        # Caso nao seja, salva no banco de dados e retorna sucesso
        costumer = Costumer(name=name, birthdate=birthdate, cpf=cpf, phone_number=phone_number)
        costumer.save()
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


# Cliente marcar horario:    /costumer/schedule/<int:id>
class CostumerMethodsScheduleId(MethodView):

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
