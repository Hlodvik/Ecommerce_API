from config import DM_API_KEY, DM_API_URL
from models.base import db
from flask import Flask, jsonify, abort
from models import Product, Payout
from models.associations import order_product
from models.dm_cache import DMCache
from schemas import PayoutSchema
import requests, random, string
from datetime import datetime, timezone
#see read me: @utils


def get_or_404(model, id=None, cond=None):
    if id is not None:
        instance = db.session.get(model, id)
    elif cond:
        instance = db.session.scalars(db.select(model).filter_by(**cond)).first()
    else:
        abort(404, description=f"{model.__name__} not found")  

    if not instance:
        abort(404, description=f"{model.__name__} not found")  #abort was suggested when a route was getting returned a tuple from the previous code which returned a json message and an error
    return instance

def get_all(model, filters=None, schema=None):
    query = db.select(model)
    if filters:
        query = query.filter_by(**filters)
    results = db.session.scalars(query).all()
    return jsonify(schema.dump(results)) if schema else results

def add_commit(instance):
    db.session.add(instance)
    db.session.commit()

def del_commit(instance):
    db.session.delete(instance)
    db.session.commit()

def exe_commit(conditions):
    db.session.execute(conditions)
    db.session.commit()

def check_product_dm(country_code):
    params = {
        "country": country_code,
        "api_key": DM_API_KEY
    }

    try:
        response = requests.get(DM_API_URL, params=params, timeout=1)  # quick time out since we know it wont connect
        response.raise_for_status()  
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            entry = data["results"][0]


            existing_record = dbs.execute(db.select(DMCache).filter_by(country=country_code)).one_or_none()
            if existing_record:
                existing_record.de_minimis_value = entry.get("de_minimis_value", 0)
                existing_record.de_minimis_currency = entry.get("de_minimis_currency", "USD")
                existing_record.vat_amount = entry.get("vat_amount", 0)
                existing_record.vat_currency = entry.get("vat_currency", "USD")
                existing_record.notes = entry.get("notes", "")
            else:
                db.session.add(DMCache(
                    country=entry.get("country"),
                    de_minimis_value=entry.get("de_minimis_value", 0),
                    de_minimis_currency=entry.get("de_minimis_currency", "USD"),
                    vat_amount=entry.get("vat_amount", 0),
                    vat_currency=entry.get("vat_currency", "USD"),
                    notes=entry.get("notes", "")
                ))
            db.session.commit()

            return {
                "country_name": entry.get("country_name"),
                "country": entry.get("country"),
                "de_minimis_value": entry.get("de_minimis_value", 0),
                "de_minimis_currency": entry.get("de_minimis_currency", "USD"),
                "vat_amount": entry.get("vat_amount", 0),
                "vat_currency": entry.get("vat_currency", "USD"),
                "notes": entry.get("notes", "")
            }

    except (requests.RequestException, KeyError):
        # API request failed, use last known data from the database
        last_known_data = dbs.execute(db.select(DMCache).filter_by(country=country_code)).one_or_none()
        if last_known_data:
            return {
                "country_name": last_known_data.country_name,
                "country": last_known_data.country,
                "de_minimis_value": last_known_data.de_minimis_value,
                "de_minimis_currency": last_known_data.de_minimis_currency,
                "vat_amount": last_known_data.vat_amount,
                "vat_currency": last_known_data.vat_currency,
                "notes": last_known_data.notes
            }
        else:
            # No cached data available, return default values
            return {
                "country_name": "Unknown",
                "country": country_code,
                "de_minimis_value": 0,
                "de_minimis_currency": "USD",
                "vat_amount": 0,
                "vat_currency": "USD",
                "notes": "No data available"
            }

def products_to_order(order, products):
    for product_data in products:
        product = get_or_404(Product, product_data["product_id"])
        quantity = product_data.get("quantity", 1)
        existing_entry = dbs.execute(order_product.select().where(order_product.c.order_id == order.id, order_product.c.product_id == product.id)).one_or_none()

        if existing_entry:
            exe_commit(order_product.update().where(order_product.c.order_id == order.id, order_product.c.product_id == product.id).values(quantity=existing_entry.quantity + quantity))
        else:
            exe_commit(order_product.insert().values(order_id=order.id, product_id=product.id, quantity=quantity))
    
def apply_dm_taxes(order):
    if order.shipping_address is None:
        return 
    country_code = order.shipping_address.country_code  
    tax_data = check_product_dm(country_code)

    vat_percentage = tax_data.get("vat_amount", 0)  # VAT %
    de_minimis_threshold = tax_data.get("de_minimis_value", 0)  
    product_entries = dbs.execute(order_product.select().where(order_product.c.order_id == order.id)).fetchall()
    order_total = sum(entry.quantity * dbs.execute(Product.select().where(Product.id == entry.product_id)).scalar_one().price for entry in product_entries)  
    if order_total > de_minimis_threshold:  # pass the thresh, apply the tax
        for entry in product_entries:
            product_price = dbs.execute(Product.select().where(Product.id == entry.product_id)).scalar_one().price
            product_total = entry.quantity * product_price

            vat_amount = (vat_percentage / 100) * product_total if vat_percentage else 0
            exe_commit(order_product.update().where(order_product.c.order_id == order.id, order_product.c.product_id == entry.product_id).values(export_tax=vat_amount))

def generate_transaction_id() -> str: 
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"TXN-{random_str}-{timestamp}"

def create_payout(data: dict) -> Payout:
    payout_data = PayoutSchema.load(data)
    payout_data.amount = payout_data.payment.amount
    payout_data.transaction_id = generate_transaction_id()
    db.session.add(payout_data)
    db.session.commit()
    return payout_data

dbs = db.session