from app.extensions import db

# Modelo base para ser herdado por classes
class BaseModel(db.Model):
    __abstract__ = True

    @staticmethod
    def delete(obj):
        db.session.delete(obj)
        db.session.commit()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()



# Classe para ser herdada por Employee e Costumer
class UserModel(BaseModel):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    birthdate = db.Column(db.String)
    cpf = db.Column(db.Integer, nullable=False, unique=True)
    phone_number = db.Column(db.String)