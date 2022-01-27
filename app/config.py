from app.sensive import Sensive

class Config:
    # Configuracoes flask e sql 
    DEBUG = Sensive.DEBUG
    SQLALCHEMY_DATABASE_URI = Sensive.SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = Sensive.SQLALCHEMY_TRACK_MODIFICATIONS

    # Configuracoes email
    MAIL_SERVER = Sensive.MAIL_SERVER
    MAIL_PORT = Sensive.MAIL_PORT
    MAIL_USERNAME = Sensive.MAIL_USERNAME
    MAIL_USE_TLS = Sensive.MAIL_USE_TLS
    MAIL_USE_SSL = Sensive.MAIL_USE_SSL

    MAIL_PASSWORD = Sensive.MAIL_PASSWORD

    JWT_SECRET_KEY = Sensive.JWT_SECRET_KEY