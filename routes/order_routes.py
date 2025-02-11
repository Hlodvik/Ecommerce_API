from flask import Blueprint, request, jsonify
from models.order import Order
from models.product import Product
from models.associations import order_product
from schemas import OrderSchema, ProductSchema
from extensions import db
from utils import get_or_404, get_all, add_commit, del_commit, exe_commit, dbs, order_products, apply_dm_taxes

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
products_schema = ProductSchema(many=True)

bp = Blueprint("order_routes", __name__, url_prefix="/orders")

#create order
@bp.route("/", methods=["POST"])
def create_order():
    data = request.get_json()
    fields = ("user_id", "shipping_address_id", "payment_id", "products")

    if any(field not in data for field in fields):
        return jsonify({"message": "Missing fields"}), 400

    new_order = Order(**{field: data[field] for field in fields}, status=data.get("status", "pending"))

    for product_data in data["products"]:
        product = get_or_404(Product, product_data["product_id"])
        quantity = product_data.get("quantity", 1)
        dbs.execute(order_product.insert().values(order_id=new_order.id, product_id=product.id, quantity=quantity))

    apply_dm_taxes(new_order)
    add_commit(new_order)

    return jsonify(order_schema.dump(new_order)), 201



# get all orders 
@bp.route("/", methods=["GET"])
def get_orders():
    return get_all(Order, schema=orders_schema)

# get a specific order
@bp.route("/<int:order_id>/", methods=["GET"])
def get_order(order_id):
    order = get_or_404(Order, order_id)
    return jsonify(order_schema.dump(order))



# update order 
@bp.route("/<int:order_id>/", methods=["PUT"])
def update_order(order_id):
    order = get_or_404(Order, order_id)
    data = request.get_json()
    fields = {"status", "shipping_address_id", "payment_id"}
    for field in fields:
        if field in data:
            setattr(order, field, data[field])
    dbs.commit()
    return jsonify(order_schema.dump(order))

# delete an order
@bp.route("/<int:order_id>/", methods=["DELETE"])
def delete_order(order_id):
    order = get_or_404(Order, order_id)
    del_commit(order)
    return "", 204




#==============================Order/product table routes===================================#

#create item in order
@bp.route("/<int:order_id>/items/", methods=["POST"])
def add_to_order(order_id):
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)
    order = get_or_404(Order, order_id)
    product = get_or_404(Product, product_id)

    order_products(order, [data])
    return jsonify({"message": "Product added to order"}), 201

# get item 
@bp.route("/<int:order_id>/products/", methods=["GET"])
def get_order_products(order_id):
    order = get_or_404(Order, order_id)  # do I exist?
    product_ids = [row.product_id for row in dbs.execute(order_product.select().where(order_product.c.order_id == order.id)).scalars().all()]# get product id's from order
    if not product_ids:
        return jsonify({"message": "No products found in this order"}), 404
    return get_all(Product, filters={"id": product_ids}, schema=products_schema)

#update item
@bp.route("/<int:order_id>/items/<int:product_id>/", methods=["PUT"])
def update_order_item(order_id, product_id):
    data = request.get_json()
    quantity = data.get("quantity")
    order = get_or_404(Order, order_id)
    product = get_or_404(Product, product_id)
    if quantity == 0:
        return remove_order_item(order_id, product_id)
    exe_commit(order_product.update().where(order_product.c.order_id == order.id, order_product.c.product_id == product.id).values(quantity=quantity))
    return jsonify({"message": "Order item updated"}), 200

#delete item
@bp.route("/<int:order_id>/items/<int:product_id>/", methods=["DELETE"])
def remove_order_item(order_id, product_id):
    order = get_or_404(Order, order_id)
    product = get_or_404(Product, product_id)
    exe_commit(order_product.delete().where(order_product.c.order_id == order.id, order_product.c.product_id == product.id))
    return "", 204