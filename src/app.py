from flask import Flask

from .config import app_config
from .models import db, bcrypt

# import user_api blueprint
from .views.UserView import user_api as user_blueprint
from .views.StoreView import store_api as store_blueprint
from .views.StoretypeView import storetype_api as storetype_blueprint


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
  app.register_blueprint(store_blueprint, url_prefix='/api/v1/stores')
  app.register_blueprint(storetype_blueprint, url_prefix='/api/v1/storetype')

  @app.route('/', methods=['GET'])
  def index():
    """
    example endpoint
    """
    return 'Congratulations! Your part 2 endpoint is working'

  return app