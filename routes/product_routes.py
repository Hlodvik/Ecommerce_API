from flask import Blueprint, request, jsonify
from models.product import Product
from schemas import ProductSchema
from models.base import db
from utils import get_or_404, add_commit, del_commit, dbs

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

bp = Blueprint("product_routes", __name__, url_prefix="/products")

# create new product
@bp.route("/", methods=["POST"])
def create_product():
    data = request.get_json()
    product_data = product_schema.load(data)  
    new_product = Product(**product_data)  #converts to product object
    add_commit(new_product)  
    return jsonify(product_schema.dump(new_product)), 201

# get all products
@bp.route("/", methods=["GET"])
def get_products():
    products = dbs.execute(db.select(Product)).scalars().all()
    return jsonify(products_schema.dump(products))

# get a product 
@bp.route("/<int:product_id>/", methods=["GET"])
def get_product(product_id):
    product = get_or_404(Product, product_id)
    return jsonify(product_schema.dump(product))

# update a product
@bp.route("/<int:product_id>/", methods=["PATCH"])
def update_product(product_id):
    product = get_or_404(Product, product_id)
    data = request.get_json()
    for key, value in data.items():
        if hasattr(product, key):
            setattr(product, key, value)
    dbs.commit()
    return jsonify(product_schema.dump(product))

# delete a product
@bp.route("/<int:product_id>/", methods=["DELETE"])
def delete_product(product_id):
    product = get_or_404(Product, product_id)
    del_commit(product)
    return jsonify({"message": "Product deleted"}), 204