from flask import Blueprint, request, jsonify
from extensions import db
from models import Payout, Payment
from schemas import PayoutSchema
from utils import get_all, get_or_404, add_commit, del_commit, dbs
payout_schema = PayoutSchema()

bp = Blueprint("payout_routes", __name__, url_prefix="/payouts")

#create payout
@bp.route("/", methods=["POST"])
def create_payout():
    data = request.get_json()
    payment = get_or_404(Payment, lookup={"order_id": data.get("order_id")})
    new_payout = Payout(order_id=payment.order.id, payment_id=payment.id, seller_id=data.get("seller_id"), amount=payment.amount, transaction_id=data["transaction_id"],status=data.get("status"))

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