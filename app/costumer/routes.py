from app.extensions import Blueprint
from app.costumer.controller import CostumerMethods, CostumerMethodsId, CostumerMethodsScheduleCpf

costumer_api = Blueprint("costumer_api", __name__)

costumer_api.add_url_rule("/costumer", view_func = CostumerMethods.as_view('geralCliente'), methods=['GET', 'POST'])
costumer_api.add_url_rule("/costumer/<int:id>", view_func = CostumerMethodsId.as_view('geralClienteId'), methods=['GET', 'PATCH', 'DELETE'])
costumer_api.add_url_rule("/costumer/schedule/<int:cpf>", view_func = CostumerMethodsScheduleCpf.as_view('geralClienteIdCpf'), methods=['PATCH'])
