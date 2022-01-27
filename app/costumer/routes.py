from app.extensions import Blueprint
from app.costumer.controller import CostumerLogin, CostumerMethods, CostumerMethodsId, CostumerMethodsScheduleId

costumer_api = Blueprint("costumer_api", __name__)

costumer_api.add_url_rule("/costumer", view_func = CostumerMethods.as_view('geralCliente'), methods=['GET', 'POST'])
costumer_api.add_url_rule("/costumer/<int:id>", view_func = CostumerMethodsId.as_view('geralClienteId'), methods=['GET', 'PATCH', 'DELETE'])
costumer_api.add_url_rule("/costumer/schedule/<int:id>", view_func = CostumerMethodsScheduleId.as_view('geralClienteScheduleId'), methods=['PATCH'])
costumer_api.add_url_rule("/costumer/login", view_func = CostumerLogin.as_view('geralClienteLogin'), methods=['POST'])
