from flask import Blueprint, request, jsonify
from models.user import User
from schemas import UserSchema
from extensions import db
from utils import get_or_404, add_commit

user_schema = UserSchema()
users_schema = UserSchema(many=True)

bp = Blueprint("user_routes", __name__, url_prefix="/users")

# create user
@bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = user_schema.load(data)
    add_commit(new_user)
    return jsonify(user_schema.dump(new_user)), 201

# get all users
@bp.route("/", methods=["GET"])
def get_users():
    users = db.session.scalars(db.select(User)).all()
    return jsonify(users_schema.dump(users))

# get user by id
@bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = get_or_404(User, user_id)
    return jsonify(user_schema.dump(user))

# update user
@bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = get_or_404(User, user_id)
    data = request.get_json()
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    db.session.commit()
    return jsonify(user_schema.dump(user))

# delete user
@bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 204
