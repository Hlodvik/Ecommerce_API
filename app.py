from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from services.dm_service import seed_dm_cache
from flask_migrate import Migrate
from routes import user_routes, product_routes, order_routes, cart_routes, payment_routes, storefront_routes, address_routes
import config
from extensions import db

app = Flask(__name__)
app.config.from_object(config)

 
ma = Marshmallow(app)
migrate = Migrate(app, db)  # Enable Flask-Migrate
db.init_app(app)
# SEE README @BLUEPRINTS
app.register_blueprint(user_routes.bp)
app.register_blueprint(product_routes.bp)
app.register_blueprint(order_routes.bp)
app.register_blueprint(cart_routes.bp)
app.register_blueprint(payment_routes.bp)
app.register_blueprint(storefront_routes.bp)
app.register_blueprint(address_routes.bp)

 



if __name__ == "__main__":
    with app.app_context():
        from services.dm_service import seed_dm_cache 
        seed_dm_cache()#populates the cache on init with hardcoded data based on what I gathered online
    app.run(debug=True)