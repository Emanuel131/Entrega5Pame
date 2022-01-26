from app.models import UserModel
from app.extensions import db

class Costumer(UserModel):
    __tablename__ = "costumer"

    # Hora que comeca a aula marcada
    init_time_scheduled = db.Column(db.String, default="")  
    # Hora que termina a aula marcada
    final_time_scheduled = db.Column(db.String, default="")  

    def json(self):
        return {
            "id":self.id,
            "name":self.name,
            "birthdate":self.birthdate,
            "cpf":self.cpf,
            "phone_number":self.phone_number,
            "init_time_scheduled":self.init_time_scheduled,
            "final_time_scheduled":self.final_time_scheduled
        }
    