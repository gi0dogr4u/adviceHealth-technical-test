from flasgger.utils import swag_from
from flask import request, jsonify, Blueprint
from pydantic import ValidationError

from . import db
from .models import CarOwner, Car
from .schemas import OwnerCreate, CarCreate, OwnerResponse, CarResponse


bp = Blueprint('main', __name__)


@bp.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify({'error': e.errors()}), 400


@swag_from('docs/api_docs.yaml')
@bp.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to City Car Management API!'}), 200


@swag_from('docs/api_docs.yaml')
@bp.route('/owners', methods=['POST'])
def add_owner():
    try:
        data = OwnerCreate.parse_obj(request.json)
        owner = CarOwner(name=data.name)
        db.session.add(owner)
        db.session.commit()
        return OwnerResponse(id=owner.id, name=owner.name).dict(), 201
    except ValidationError as e:
        return handle_validation_error(e)


@swag_from('docs/api_docs.yaml')
@bp.route('/owners', methods=['GET'])
def get_owners():
    owners = CarOwner.query.all()
    return jsonify([OwnerResponse(id=owner.id, name=owner.name).dict() for owner in owners]), 200


@swag_from('docs/api_docs.yaml')
@bp.route('/cars', methods=['POST'])
def add_car():
    try:
        data = CarCreate.parse_obj(request.json)
        owner = CarOwner.query.get(data.owner_id)

        if not owner:
            return jsonify({'error': 'Owner not found'}), 404

        if not owner.can_add_car():
            return jsonify({'error': 'Owner already has 3 cars'}), 400

        car = Car(color=data.color, model=data.model, owner_id=owner.id)
        db.session.add(car)
        db.session.commit()

        return CarResponse(id=car.id, color=car.color, model=car.model, owner_id=owner.id, owner_name=owner.name).dict(), 201
    except ValidationError as e:
        return handle_validation_error(e)


@swag_from('docs/api_docs.yaml')
@bp.route('/cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    result = [{
        'id': car.id,
        'color': car.color,
        'model': car.model,
        'owner_id': car.owner_id,
        'owner_name': car.owner.name
    } for car in cars]
    return jsonify(result), 200


@swag_from('docs/api_docs.yaml')
@bp.route('/owners/sales_opportunities', methods=['GET'])
def sales_opportunities():
    owners = CarOwner.query.all()
    opportunities = [{
        'id': owner.id,
        'name': owner.name
    } for owner in owners if not owner.cars]

    return jsonify(opportunities), 200


def register_routes(app):
    app.register_blueprint(bp)
