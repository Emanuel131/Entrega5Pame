from app.models import UserModel

class Employee(UserModel):
    __tablename__ = "employee"
    
    def json(self):
        return {
            "id":self.id,
            "name":self.name,
            "birthdate":self.birthdate,
            "cpf":self.cpf,
            "phone_number":self.phone_number
        }
    