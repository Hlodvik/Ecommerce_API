from flask import Blueprint, request, jsonify
from models import Address, User
from schemas import AddressSchema
from models.base import db
from utils import dbs, add_commit, del_commit
address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)

bp = Blueprint("address_routes", __name__, url_prefix="/addresses")

# create new address for the user
@bp.route("/users/<int:user_id>/addresses/", methods=["POST"])
def add_address(user_id):
    data = request.get_json()
    user = db.session.get(User, user_id)
    if not user:#no unpaired addresses allowed
        return jsonify({"message": "user not found"}), 404

    new_address = address_schema.load({"user_id": user.id, **data})
    db.session.add(new_address)
    db.session.commit()

    return jsonify(address_schema.dump(new_address)), 201

# get all addresses, filter by user id
@bp.route("/", methods=["GET"])
def get_addresses():
    user_id = request.args.get("user_id")
    if user_id:
        addresses = db.session.execute(db.select(Address).filter_by(user_id=user_id)).scalars().all()
    else:
        addresses = db.session.execute(db.select(Address)).scalars().all()
    
    return jsonify(addresses_schema.dump(addresses))

# get address
@bp.route("/<int:address_id>/", methods=["GET"])
def get_address(address_id):
    address = db.session.get(Address, address_id)
    if not address:
        return jsonify({"message": "Address not found"}), 404
    return jsonify(address_schema.dump(address))

#edit/update address
@bp.route("/addresses/<int:address_id>/", methods=["PUT"])
def update_address(address_id):
    data = request.get_json()
    
    address = db.session.get(Address, address_id)
    if not address:
        return jsonify({"message": "Address not found"}), 404
    
    address.street = data.get("street", address.street)
    address.city = data.get("city", address.city)
    address.region = data.get("region", address.region)
    address.country = data.get("country", address.country)
    address.zipcode = data.get("zipcode", address.zipcode)
    
    db.session.commit()
    return jsonify(address_schema.dump(address))

#delete address
@bp.route("/addresses/<int:address_id>/", methods=["DELETE"])
def delete_address(address_id):
    address = db.session.get(Address, address_id)
    if not address:
        return jsonify({"message": "Address not found"}), 404
    db.session.delete(address)
    db.session.commit()

    return "", 204