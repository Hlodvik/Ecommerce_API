from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from models import Storefront, User
from schemas import StorefrontSchema, UserSchema
from extensions import db
from utils import get_or_404, del_commit, add_commit, dbs

storefront_schema = StorefrontSchema()
storefronts_schema = StorefrontSchema(many=True)
users_schema = UserSchema(many=True)
bp = Blueprint("storefront_routes", __name__, url_prefix="/storefronts")

# create storefront
@bp.route("/", methods=["POST"])
def create_storefront():
    data = request.get_json()
    loaded_data = storefront_schema.load(data)
    if isinstance(loaded_data, dict):
        new_storefront = Storefront(**loaded_data)
    else:
        new_storefront = loaded_data

    add_commit(new_storefront)
    return jsonify(storefront_schema.dump(new_storefront)), 201



# get all storefronts
@bp.route("/", methods=["GET"])
def get_storefronts():
    storefronts = dbs.execute(db.select(Storefront)).scalars().all()
    return jsonify(storefronts_schema.dump(storefronts))

# get a storefront
@bp.route("/<int:storefront_id>/", methods=["GET"])
def get_storefront(storefront_id):
    storefront = get_or_404(Storefront, storefront_id)

    return jsonify(storefront_schema.dump(storefront))

#update storefront
@bp.route("/<int:storefront_id>/", methods=["PATCH"])
def update_storefront(storefront_id):
    storefront = get_or_404(Storefront, storefront_id)
    data = request.get_json()
    fields = {"name", "business_info_id"}  
    for field in fields:
        if field in data:
            setattr(storefront, field, data[field])
    dbs.commit()
    return jsonify(storefront_schema.dump(storefront)), 200

#delete storefront
@bp.route("/<int:storefront_id>/", methods=["DELETE"])
def delete_storefront(storefront_id):
    storefront = get_or_404(Storefront, storefront_id)
    del_commit(storefront)   
    return "", 204  

#===================storefront/user table routes=====================#
#create admin
@bp.route("/<int:storefront_id>/admins/", methods=["POST"])
def add_storefront_admin(storefront_id):
    data = request.get_json()
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"message": "Missing user_id"}), 400

    storefront = get_or_404(Storefront, storefront_id)
    admin = get_or_404(User, user_id)
    if admin in storefront.admins:
        return jsonify({"message": "User is already an admin"}), 400

    storefront.admins.append(admin) 
    dbs.commit()
    return jsonify({"message": "Admin added"}), 201
#get admins
@bp.route("/<int:storefront_id>/admins/", methods=["GET"])
def get_storefront_admins(storefront_id):
    storefront = get_or_404(Storefront, storefront_id)
    return jsonify(users_schema.dump(storefront.admins)), 200

#remove admin
@bp.route("/<int:storefront_id>/admins/<int:user_id>/", methods=["DELETE"])
def remove_storefront_admin(storefront_id, user_id):
    storefront = get_or_404(Storefront, storefront_id)
    admin = get_or_404(User, user_id)
    if admin not in storefront.admins:
        return jsonify({"message": "User is not an admin"}), 400

    storefront.admins.remove(admin)  
    dbs.commit()
    return "", 204