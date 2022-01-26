from app.models import BaseModel
from app.extensions import db

class Product(BaseModel):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    quantity = db.Column(db.Float)
    description = db.Column(db.String)
    valid_through = db.Column(db.String)
    lastModifiedByCpf = db.Column(db.String)
    

    def json(self):
        return {
            "id":self.id,
            "name":self.name,
            "quantity":self.quantity,
            "description":self.description,
            "valid_through":self.valid_through,
            "lastModifiedByCpf":self.lastModifiedByCpf
        }
    