# Importa extensoes necessarias
from flask import Flask, Blueprint, request
from flask.views import MethodView

from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
