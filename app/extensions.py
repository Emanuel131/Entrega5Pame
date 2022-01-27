# Importa extensoes necessarias
from flask import Flask, Blueprint, request, render_template
from flask.views import MethodView

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_mail import Mail, Message

import bcrypt


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
jwt = JWTManager()
