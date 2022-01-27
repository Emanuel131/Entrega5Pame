from app.product.models import Product
from app.employee.models import Employee
from app.extensions import request, MethodView, jwt_required

# Autorizado cadastra/visualiza produto
# /product/<int:id_employee>
class ProductMethodsId(MethodView): 
    decorators = [jwt_required()]
    # Cria novo produto
    def post(self, id):
        body = request.json

        employee = Employee.query.get_or_404(id)

        name = body.get("name")
        quantity = body.get("quantity")
        description = body.get("description")
        valid_through = body.get("valid_through")

        # Verifica se dado e do tipo esperado, caso seja retorna erro
        if not isinstance(name, str) or not isinstance(quantity, float) or not isinstance(description, str) or not isinstance(valid_through, str):
            return {"code_status":"invalid data"}, 400
        
        # Caso nao seja, salva no banco de dados e retorna sucesso
        product = Product(name=name, quantity=quantity, description=description, valid_through=valid_through, lastModifiedByCpf=employee.cpf)
        product.save()

        return product.json(), 200


    # Retorna info de produtos
    def get(self, id):
        Employee.query.get_or_404(id)

        products = Product.query.all()
        body = {}

        for product in products:
            body[product.id] = product.json()
        
        return body



# Autorizado escolhe produto especifico para mostrar/alterar/deletar
# /product/<int:id_employee>/<int:id_product>
class ProductMethodsId2(MethodView):
    decorators = [jwt_required()]
    # Retorna info do banco de dados de id especifico
    def get(self, id_product, id_employee):
        product = Product.query.get_or_404(id_product)

        return product.json()


    # Altera informacoes do produto
    def patch(self, id_product, id_employee):
        body = request.json

        product = Product.query.get_or_404(id_product)
        employee = Employee.query.get_or_404(id_employee)

        name = body.get("name", product.name)
        quantity = body.get("quantity", product.quantity)
        description = body.get("description", product.description)
        valid_through = body.get("valid_through", product.valid_through)

        # Verifica se dado e do tipo esperado, caso seja retorna erro
        if not isinstance(name, str) or not isinstance(quantity, float) or not isinstance(description, str) or not isinstance(valid_through, str):
            return {"code_status":"invalid data"}, 400
        
        product.name = name
        product.quantity = quantity
        product.description = description
        product.valid_through = valid_through
        product.lastModifiedBy = employee.cpf
        product.update()

        return product.json(), 200
    

    # Deleta produto
    def delete(self, id_product, id_employee):
        product = Product.query.get_or_404(id_product)
        product.delete(product)

        return {"code_status":"deleted"}, 200
