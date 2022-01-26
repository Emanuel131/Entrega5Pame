from app.product.models import Product
from app.employee.models import Employee
from app.extensions import request, MethodView

# /product/<int:id_employee>
# Recebe id do empregado para autorização
class ProductMethodsCpf(MethodView): 

    # Insere info no banco de dados
    def post(self, id):
        body = request.json

        employee = Employee.query.get_or_404(id)

        name = body.get("name")
        quantity = body.get("quantity")
        description = body.get("description")

        # Verifica se dado e do tipo esperado, caso seja retorna erro
        if not isinstance(name, str) or not isinstance(quantity, float) or not isinstance(description, str):
            return {"code_status":"invalid data"}, 400
        
        # Caso nao seja, salva no banco de dados e retorna sucesso
        product = Product(name=name, quantity=quantity, description=description, lastModifiedByCpf=employee.cpf)
        product.save()

        return product.json(), 200


    # Retorna info do banco de dados
    def get(self, id):
        Employee.query.get_or_404(id)

        products = Product.query.all()
        body = {}

        for product in products:
            body[product.id] = product.json()
        
        return body



# /product/<int:id>/<int:id>
# Autoriza e escolhe produto especifico para mostrar
class ProductMethodsId(MethodView):

    # Retorna info do banco de dados de id especifico
    def get(self, id_product, id_employee):
        product = Product.query.get_or_404(id_product)

        return product.json()


    # Altera informacoes do produto
    def patch(self, id_product, id_employee):
        body = request.json

        product = Product.query.get_or_404(id_product)
        employee = Employee.query.get_or_404(id_employee)

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
        product.update()

        return product.json(), 200
    

    # Deleta produto
    def delete(self, id_product, id_employee):
        product = Product.query.get_or_404(id_product)
        product.delete(product)

        return {"code_status":"deleted"}, 200
