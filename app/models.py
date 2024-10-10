from . import db


class CarOwner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cars = db.relationship('Car', backref='owner', lazy=True)

    def can_add_car(self):
        return len(self.cars) < 3


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('car_owner.id'), nullable=False)

    def __init__(self, color, model, owner_id):
        self.color = color
        self.model = model
        self.owner_id = owner_id
