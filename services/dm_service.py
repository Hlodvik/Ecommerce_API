import requests
import os
from extensions import db
from models.dm_cache import DMCache 
from utils import dbs
from config import DM_API_KEY, DM_API_URL

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
        last_known_data = dbs.scalars(db.select(DMCache).filter_by(country=country_code)).scalar_one_or_none()
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
        



def seed_dm_cache():
    """searched online for data to plug in, these are real values."""
     
    preloaded_data = [
        {"country": "US", "country_name": "United States",
        "de_minimis_value": 800, "de_minimis_currency": "USD",
        "vat_amount": 0, "vat_currency": "N/A",
        "notes": "Duty applies when exceeding $800."},

        {"country": "AU", "country_name": "Australia",
        "de_minimis_value": 1000, "de_minimis_currency": "AUD",
        "vat_amount": 10, "vat_currency": "AUD",
        "notes": "Duty and taxes apply after AUD 1,000."},

        {"country": "CA", "country_name": "Canada",
        "de_minimis_value": 20, "de_minimis_currency": "CAD",
        "vat_amount": 5, "vat_currency": "CAD",
        "notes": "GST applies above CAD 20."},

        {"country": "EU", "country_name": "European Union",
        "de_minimis_value": 0, "de_minimis_currency": "EUR",
        "vat_amount": 0, "vat_currency": "EUR",
        "notes": "All imports are subject to VAT."},

        {"country": "JP", "country_name": "Japan",
        "de_minimis_value": 10000, "de_minimis_currency": "JPY",
        "vat_amount": 10, "vat_currency": "JPY",
        "notes": "Consumption tax applies above ¥10,000."},

        {"country": "CN", "country_name": "China",
        "de_minimis_value": 50, "de_minimis_currency": "CNY",
        "vat_amount": 13, "vat_currency": "CNY",
        "notes": "Duty/tax amount, not goods value."},

        {"country": "CL", "country_name": "Chile",
        "de_minimis_value": 40, "de_minimis_currency": "USD",
        "vat_amount": 19, "vat_currency": "CLP",
        "notes": "Approximately USD 41 as of 5 April 2023."},

        {"country": "CO", "country_name": "Colombia",
        "de_minimis_value": 200, "de_minimis_currency": "USD",
        "vat_amount": 19, "vat_currency": "COP",
        "notes": ""},

        {"country": "KR", "country_name": "South Korea",
        "de_minimis_value": 150, "de_minimis_currency": "USD",
        "vat_amount": 10, "vat_currency": "KRW",
        "notes": "Only for trade with USA and Puerto Rico as per Korea-US FTA."},

        {"country": "IL", "country_name": "Israel",
        "de_minimis_value": 75, "de_minimis_currency": "USD",
        "vat_amount": 17, "vat_currency": "ILS",
        "notes": ""},

        {"country": "NZ", "country_name": "New Zealand",
        "de_minimis_value": 1000, "de_minimis_currency": "NZD",
        "vat_amount": 15, "vat_currency": "NZD",
        "notes": "For customs duties only. GST is charged for registered overseas vendors from 1 Dec 2019."},

        {"country": "SG", "country_name": "Singapore",
        "de_minimis_value": 400, "de_minimis_currency": "SGD",
        "vat_amount": 7, "vat_currency": "SGD",
        "notes": ""},

        {"country": "CH", "country_name": "Switzerland",
        "de_minimis_value": 62, "de_minimis_currency": "CHF",
        "vat_amount": 7.7, "vat_currency": "CHF",
        "notes": ""},

        {"country": "NO", "country_name": "Norway",
        "de_minimis_value": 350, "de_minimis_currency": "NOK",
        "vat_amount": 25, "vat_currency": "NOK",
        "notes": ""},

        {"country": "MX", "country_name": "Mexico",
        "de_minimis_value": 50, "de_minimis_currency": "USD",
        "vat_amount": 16, "vat_currency": "MXN",
        "notes": ""}
    ]
    for entry in preloaded_data:
    # Check if the country already exists
        existing_record = dbs.execute(db.select(DMCache).filter_by(country=entry["country"])).one_or_none()
        if not existing_record:
            dbs.execute(db.insert(DMCache).values(entry))


    dbs.commit()
 