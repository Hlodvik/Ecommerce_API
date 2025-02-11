from flask import Blueprint, request, jsonify
from models import  Cart, Product, User, Address
from services.dm_service import check_product_dm
from models.associations import cart_product
from schemas import CartSchema, ProductSchema
from extensions import db
from utils import get_or_404, get_all, dbs, add_commit, exe_commit, del_commit

cart_schema = CartSchema()
products_schema = ProductSchema(many=True)
bp = Blueprint("cart_routes", __name__, url_prefix="/cart")

#create a cart
@bp.route("/", methods=["POST"])
def create_cart():
    data = request.get_json()
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"message": "Missing user_id"}), 400
    
    user = get_or_404(User, user_id)
    existing_cart = dbs.execute(db.select(Cart).filter_by(user_id=user_id)).scalar_one_or_none()
    if existing_cart:
        return jsonify({"message": "User already has a cart"}), 400

    new_cart = add_commit(Cart(user_id=user.id))
    return jsonify(cart_schema.dump(new_cart)), 201

#get cart
@bp.route("/<int:user_id>/", methods=["GET"])
def get_cart(user_id):
    cart = get_or_404(Cart, filters={"user_id": user_id})
    return jsonify(cart_schema.dump(cart))

#delete cart
@bp.route("/<int:user_id>/", methods=["DELETE"])
def delete_cart(user_id):
    cart = get_or_404(Cart, filters={"user_id": user_id})  # Ensure cart exists
    del_commit(cart)  # Delete and commit
    return "", 204



#=================cart/product table================
#create item
@bp.route("/<int:user_id>/items/", methods=["POST"])
def add_to_cart(user_id):
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)
    if not product_id or quantity < 1:
        return jsonify({"message": "Invalid product_id or quantity"}), 400

    cart = get_or_404(Cart, filters={"user_id": user_id})
    product = get_or_404(Product, product_id)
    address = dbs.execute(db.select(Address).filter_by(user_id=user_id, is_default=True)).scalar_one_or_none()
    country_code = address.country 
    dm_data = check_product_dm(country_code)
    if product.price > dm_data["de_minimis_value"]:
        adjusted_price = product.price + (dm_data["vat_amount"] / 100 * product.price)  # Apply VAT
        return jsonify({
            "original_price": product.price,
            "adjusted_price": round(adjusted_price, 2),
            "vat_amount": dm_data["vat_amount"],
            "vat_currency": dm_data["vat_currency"],
            "de_minimis_value": dm_data["de_minimis_value"],
            "de_minimis_currency": dm_data["de_minimis_currency"]
        }), 200   


    existing_item = db.session.execute(cart_product.select().where(cart_product.c.cart_id == cart.id, cart_product.c.product_id == product.id)).scalar_one_or_none()
    if existing_item:
        return jsonify({"message": "Product is already in cart"}), 400

    exe_commit(cart_product.insert().values(cart_id=cart.id, product_id=product.id, quantity=quantity))
    return jsonify({"message": "Product added to cart"}), 201

#get items in cart
@bp.route("/<int:user_id>/items/", methods=["GET"])
def get_cart_items(user_id):
    cart = get_or_404(Cart, filters={"user_id": user_id}) 
    product_ids = [row.product_id for row in db.session.execute(cart_product.select().where(cart_product.c.cart_id == cart.id)).scalars().all()]
    if not product_ids:
        return jsonify({"message": "Cart is empty"}), 200   

    return get_all(Product, filters={"id": product_ids}, schema=products_schema)


#update items
@bp.route("/<int:user_id>/items/<int:product_id>/", methods=["PUT"])
def update_cart_item(user_id, product_id):
    data = request.get_json()
    quantity = data.get("quantity")
    if not isinstance(quantity, int) or quantity < 1:
        return jsonify({"message": "Invalid quantity"}), 400

    cart = get_or_404(Cart, filters={"user_id": user_id})
    product = get_or_404(Product, product_id)
    existing_item = dbs.execute(cart_product.select().where(cart_product.c.cart_id == cart.id, cart_product.c.product_id == product.id)).scalar_one_or_none()
    if not existing_item:
        return jsonify({"message": "Product is not in the cart"}), 400

    exe_commit(cart_product.update().where(cart_product.c.cart_id == cart.id, cart_product.c.product_id == product.id).values(quantity=quantity))
    return jsonify({"message": "Cart item updated"}), 200


@bp.route("/<int:user_id>/items/<int:product_id>/", methods=["DELETE"])
def remove_from_cart(user_id, product_id):
    cart = get_or_404(Cart, filters={"user_id": user_id})
    product = get_or_404(Product, product_id)
    existing_item = dbs.execute(cart_product.select().where(cart_product.c.cart_id == cart.id, cart_product.c.product_id == product.id)).scalar_one_or_none()
    if not existing_item:
        return jsonify({"message": "Product is not in the cart"}), 400

    exe_commit(cart_product.delete().where(cart_product.c.cart_id == cart.id, cart_product.c.product_id == product.id))
    return "", 204 