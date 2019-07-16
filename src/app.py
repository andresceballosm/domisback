from flask import Flask

from .config import app_config
from .models import db, bcrypt

# import user_api blueprint
from .views.UserView import user_api as user_blueprint
from .views.AddressView import address_api as address_blueprint
from .views.StoreView import store_api as store_blueprint
from .views.StoretypeView import storetype_api as storetype_blueprint
from .views.CategoryView import category_api as category_blueprint
from .views.ProductView import product_api as product_blueprint
from .views.OrderView import order_api as order_blueprint
from .views.OrderDetailsView import orderDetails_api as orderDetails_blueprint

def create_app(env_name):
  """
  Create app
  """
  
  # app initiliazation
  app = Flask(__name__)

  app.config.from_object(app_config[env_name])

  # initializing bcrypt and db
  bcrypt.init_app(app)
  db.init_app(app)

  app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
  app.register_blueprint(address_blueprint, url_prefix='/api/v1/address')
  app.register_blueprint(store_blueprint, url_prefix='/api/v1/stores')
  app.register_blueprint(storetype_blueprint, url_prefix='/api/v1/storetype')
  app.register_blueprint(category_blueprint, url_prefix='/api/v1/categories')
  app.register_blueprint(product_blueprint, url_prefix='/api/v1/products')
  app.register_blueprint(order_blueprint, url_prefix='/api/v1/orders')
  app.register_blueprint(orderDetails_blueprint, url_prefix='/api/v1/orderdetails')

  @app.route('/', methods=['GET'])
  def index():
    """
    example endpoint
    """
    return 'Congratulations! Your backend Domis endpoint is working'

  return app