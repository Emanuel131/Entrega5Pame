from app.product.models import Product
from app.employee.models import Employee
from app.extensions import request, MethodView

# /product/<int:cpf>
class ProductMethodsCpf(MethodView): 

    # Insere info no banco de dados
    def post(self, cpf):
        body = request.json

        employee = Employee.query.get_or_404(cpf)

        name = body.get("name")
        quantity = body.get("quantity")
        description = body.get("description")

        # Verifica se dado e do tipo esperado, caso seja retorna erro
        if not isinstance(name, str) or not isinstance(quantity, float) or not isinstance(description, str):
            return {"code_status":"invalid data"}, 400
        
        # Caso nao seja, salva no banco de dados e retorna sucesso
        product = Product(name=name, quantity=quantity, description=description, lastModifiedBy=employee.cpf)
        product.save()

        return product.json(), 200


    # Retorna info do banco de dados
    def get(self):
        products = Product.query.all()
        body = {}

        for product in products:
            body[product.id] = product.json()
        
        return body



# /product/<int:id>/<int:cpf>
class ProductMethodsId(MethodView):

    # Retorna info do banco de dados de id especifico
    def get(self, id):
        product = Product.query.get_or_404(id)

        return product.json()


    # Altera informacoes do produto
    def patch(self, id, cpf):
        body = request.json

        product = Product.query.get_or_404(id)
        employee = Employee.query.get_or_404(cpf)

        name = body.get("name")
        quantity = body.get("quantity")
        description = body.get("description")

        # Verifica se dado e do tipo esperado, caso seja retorna erro
        if not isinstance(name, str) or not isinstance(quantity, float) or not isinstance(description, str):
            return {"code_status":"invalid data"}, 400
        
        product.name = name
        product.quantity = quantity
        product.description = description
        product.lastModifiedBy = employee.cpf

        return product.json(), 200
    

    # Deleta produto
    def delete(self, id):
        product = Product.query.get_or_404(id)
        product.delete(product)

        return {"code_status":"deleted"}, 200
