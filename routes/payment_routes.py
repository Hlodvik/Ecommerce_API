from flask import Blueprint, request, jsonify
from models import Payment
from schemas import PaymentSchema
from extensions import db
from utils import get_or_404, get_all, add_commit, del_commit, dbs

payment_schema = PaymentSchema()
payments_schema = PaymentSchema(many=True)

bp = Blueprint("payment_routes", __name__, url_prefix="/payments")

# create payment
@bp.route("/", methods=["POST"])
def create_payment():
    data = request.get_json()
    new_payment = payment_schema.load(data)
    add_commit(new_payment)
    return jsonify(payment_schema.dump(new_payment)), 201

#get all payments, can filt by user id
@bp.route("/", methods=["GET"])
def get_payments():
    filters = {"user_id": request.args.get("user_id")} if request.args.get("user_id") else None
    return get_all(Payment, filters=filters, schema=payments_schema)

# get payment
@bp.route("/<int:payment_id>", methods=["GET"])
def get_payment(payment_id):
    payment = get_or_404(Payment, payment_id)
    return jsonify(payment_schema.dump(payment))

# update payment 
@bp.route("/<int:payment_id>", methods=["PUT"])
def update_payment(payment_id):
    payment = get_or_404(Payment, payment_id)
    data = request.get_json()
    fields= {"status", "transaction_id", "amount"}
    for field in fields:
        if field in data:
            setattr(payment, field, data[field])
    db.session.commit()
    return jsonify(payment_schema.dump(payment))

# delete payment
@bp.route("/<int:payment_id>", methods=["DELETE"])
def delete_payment(payment_id):
    payment = get_or_404(Payment, payment_id)
    del_commit(payment)
    return "", 204