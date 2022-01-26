from app.extensions import Blueprint
from app.product.controller import ProductMethodsCpf, ProductMethodsId

product_api = Blueprint("product_api", __name__)

product_api.add_url_rule("/product/<int:cpf>", view_func = ProductMethodsCpf.as_view('geralProduto'), methods=['GET', 'POST'])
product_api.add_url_rule("/product/<int:id>/<int:cpf>", view_func = ProductMethodsId.as_view('geralProdutoIdCpf'), methods=['GET', 'PATCH', 'DELETE'])