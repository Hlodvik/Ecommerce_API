from marshmallow import Schema, fields, validate
from flask_marshmallow import Marshmallow
from marshmallow.validate import Range
ma = Marshmallow()

# ----------------- BASE -----------------#
class BaseSchema(Schema):
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True, format="%Y-%m-%d %H:%M:%S")

# ----------------- USER -----------------#
class UserSchema(BaseSchema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True, validate=validate.Length(max=150))
    addresses = fields.List(fields.Nested(lambda: AddressSchema(exclude=("user",))), dump_only=True)
    orders = fields.List(fields.Nested(lambda: OrderSchema(exclude=("user",))), dump_only=True)
    payments = fields.List(fields.Nested(lambda: PaymentSchema(exclude=("user",))), dump_only=True)
    cart = fields.Nested(lambda: CartSchema(exclude=("user",)), dump_only=True)

class SellerSchema(UserSchema):
    storefronts = fields.List(fields.Nested(lambda: StorefrontSchema(exclude=("admins",))), dump_only=True)

# ----------------- ADDRESS  -----------------#
class AddressSchema(BaseSchema):
    street = fields.Str(required=True)
    city = fields.Str(required=True)
    region = fields.Str(required=True)
    country = fields.Str(required=True)
    zipcode = fields.Str(required=True)
    user = fields.Nested(lambda: UserSchema(exclude=("addresses",)), dump_only=True)

# ----------------- STOREFRONT / BUSINESS INFO -----------------------#
class BusinessInfoSchema(BaseSchema):
    business_name = fields.Str(required=True)
    license_number = fields.Str()
    industry = fields.Str(required=True)
    tax_id = fields.Str(required=True)
    tax_status = fields.Str(required=True)
    compliance_docs = fields.Str()
    business_phone = fields.Str()
    business_email = fields.Email()
    storefront = fields.Nested(lambda: StorefrontSchema(exclude=("business_info",)), dump_only=True)

class StorefrontSchema(BaseSchema):
    name = fields.Str(required=True)
    business_info_id = fields.Int(allow_none=True)  
    business_info = fields.Nested(BusinessInfoSchema, dump_only=True)
    admins = fields.List(fields.Nested(lambda: SellerSchema(exclude=("storefronts",))), dump_only=True)
    products = fields.List(fields.Nested(lambda: ProductSchema(exclude=("storefront",))), dump_only=True)

# ----------------- PRODUCT ------------------------#
class ProductSchema(BaseSchema):
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    price = fields.Decimal(as_string=True, required=True)
    stock = fields.Int(required=True)
    hs_code = fields.Str(required=False)
    restricted = fields.Bool(default=False)
    restriction_reason = fields.Str(allow_none=True)
    storefront_id = fields.Int(required=True)     
    storefront = fields.Nested(lambda: StorefrontSchema(exclude=("products",)), dump_only=True)

# ----------------- CART & ORDER, SVU ------------------#
class CartSchema(BaseSchema):
    user = fields.Nested(lambda: UserSchema(exclude=("cart",)), dump_only=True)
    products = fields.List(fields.Nested(lambda: ProductSchema(exclude=("carts",))), dump_only=True)

class CartProductSchema(Schema):
    cart_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))

class OrderSchema(BaseSchema):
    status = fields.Str(validate=validate.OneOf(["pending", "shipped", "delivered", "cancelled"]), default="pending")
    user = fields.Nested(lambda: UserSchema(exclude=("orders",)), dump_only=True)
    shipping_address = fields.Nested(AddressSchema, dump_only=True)

    payment = fields.Nested(lambda: PaymentSchema(exclude=("order",)), dump_only=True)
    products = fields.List(fields.Nested(ProductSchema), required=True, validate=validate.Length(min=1))
    payout = fields.Nested(lambda: PayoutSchema(exclude=("order",)), dump_only=True)
    
class OrderProductSchema(Schema):
    order_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    export_tax = fields.Decimal(as_string=True)

# ----------------- PAY ---------------------#
class PaymentSchema(BaseSchema):
    amount = fields.Decimal(as_string=True, required=True, validate=Range(min=0.01))
    transaction_id = fields.Str(required=True)
    status = fields.Str(default="pending")
    user = fields.Nested(lambda: UserSchema(exclude=("payments",)), dump_only=True)
    order = fields.Nested(lambda: OrderSchema(exclude=("payment",)), dump_only=True)
    payout = fields.Nested(lambda: PayoutSchema(exclude=("payment",)), dump_only=True)

class PayoutSchema(BaseSchema):
    order = fields.Nested(lambda: OrderSchema(exclude=("payout",)), dump_only=True)
    payment = fields.Nested(lambda: PaymentSchema(exclude=("payout",)), dump_only=True)
    user = fields.Nested(lambda: UserSchema(exclude=("payouts",)), dump_only=True)
    amount = fields.Decimal(as_string=True, required=True)
    transaction_id = fields.Str(required=True)
    status = fields.Str(default="pending")

class DMCacheSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    country = fields.Str(required=True)  # ISO-2 Country Code
    de_minimis_value = fields.Float(default=0)
    de_minimis_currency = fields.Str(default="USD")
    vat_amount = fields.Float(default=0)
    vat_currency = fields.Str(default="USD")
    notes = fields.Str(default="")


# ----------------- INIT -----------------#
def init_schemas(app):
    ma.init_app(app)
