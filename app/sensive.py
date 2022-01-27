class Sensive:
    EMAIL_SENDER_NAME = "Joaquim"
    EMAIL = "emanuelaires@poli.ufrj.br"

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "smtp.sendgrid.net"
    MAIL_PORT = 465
    MAIL_USERNAME = "apikey"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    MAIL_PASSWORD = "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"

    JWT_SECRET_KEY = "iasdofihawuehgenbivjnorfvnpearijvanskllla"