from flask import Blueprint, request, jsonify
from models import Payout, Order 
from schemas import PayoutSchema
from utils import get_all, get_or_404, del_commit, dbs, create_payout
payout_schema = PayoutSchema()
bp = Blueprint("payout_routes", __name__, url_prefix="/payouts")

@bp.route("/", methods=["POST"])
def create_payout_():
    data = request.get_json()
    if "order_id" not in data:
        return jsonify({"message": "Missing order_id"}), 400

    order = get_or_404(Order, data["order_id"])
    data["storefront_id"] = order.storefront_id  
    new_payout = create_payout(data)  

    return jsonify(payout_schema.dump(new_payout)), 201

# get payout 
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