from flask import Blueprint, request, jsonify
import requests
from extensions import db
from models import Payout, Order 
from schemas import PayoutSchema
from routes.order_routes import create_order
from utils import get_all, get_or_404, add_commit, exe_commit, del_commit, dbs
payout_schema = PayoutSchema()

bp = Blueprint("payout_routes", __name__, url_prefix="/payouts")
ORDER_SERVICE_URL = "http://127.0.0.1:5000/orders/"
#create payout
@bp.route("/", methods=["POST"])
def create_payout():
    data = request.get_json()
    fields = ("order_id", "amount", "transaction_id")   

    missing_fields = [field for field in fields if field not in data]
    if missing_fields:
        return jsonify({"message": "Missing required fields", "missing": missing_fields}), 400

    # added this to test routes in postman
    if "amount" in data and "order_id" not in data:
        order_data = {
            "user_id": 1,  # Default user ID
            "shipping_address_id": None,
            "payment_id": None,
            "products": [],
            "amount": data["amount"]
        }

        response = requests.post(ORDER_SERVICE_URL, json=order_data)  
        if response.status_code != 201:
            return jsonify({"error": response.text}), response.status_code
        try:
            new_order = response.json()
        except requests.exceptions.JSONDecodeError:
            return jsonify({"error": response.text}), 500
        data["order_id"] = new_order.get("id")

    new_order = get_or_404(Order, data["order_id"])
    new_payout = Payout(order_id=new_order.id, user_id=new_order.user_id, amount=data["amount"], transaction_id=data["transaction_id"], status="pending")
    add_commit(new_payout)
    return jsonify(payout_schema.dump(new_payout)), 201

# get payout, can filter by order id
@bp.route("/", methods=["GET"])
def get_payouts():
    order_id = request.args.get("order_id")  # Optional filter
    filters = {"order_id": order_id} if order_id else None
    return get_all(Payout, filters, payout_schema)

# Update payout 
@bp.route("/<int:payout_id>/", methods=["PUT"])
def update_payout(payout_id):
    payout = get_or_404(Payout, payout_id)
    data = request.get_json()
    fields= {"status", "transaction_id", "amount"}
    for field in fields:
        if field in data:
            setattr(payout, field, data[field])
    dbs.commit()
    return jsonify(payout_schema.dump(payout))

#delete payout
@bp.route("/<int:payout_id>/", methods=["DELETE"])
def delete_payout(payout_id):
    payout = get_or_404(Payout, identifier=payout_id)
    del_commit(payout)
    return "", 204