from app.extensions import db, Flask, migrate, mail, jwt
from app.config import Config

from app.product.routes import product_api
from app.costumer.routes import costumer_api
from app.employee.routes import employee_api

# Cria app
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    jwt.init_app(app)

    # Registra blueprints
    app.register_blueprint(product_api)
    app.register_blueprint(costumer_api)
    app.register_blueprint(employee_api)


    return app