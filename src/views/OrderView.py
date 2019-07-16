from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.OrderModel import OrderModel, OrderSchema
from ..models.StoreModel import StoreModel, StoreSchema
from ..models.UserModel import UserModel, UserSchema
from ..models.CategoryModel import CategoryModel, CategorySchema
from ..models.ProductModel import ProductModel, ProductSchema

order_api = Blueprint('order_api', __name__)
order_schema = OrderSchema()
user_schema = UserSchema()
store_schema = StoreSchema()
category_schema = CategorySchema()
product_schema = ProductSchema()

def validateStore(type):
  stores = StoreModel.get_all_stores()
  data = store_schema.dump(stores, many=True).data
  for store in data:
    if store['id'] == type:
        return True

@order_api.route('/create', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create order Function
  """
  req_data = request.get_json()
  req_data['user'] = g.user.get('id')
  data, error = order_schema.load(req_data)
  storevalid = validateStore(data['store_id'])

  if storevalid == None:
    return custom_response({'error': 'store_id no existe!'}, 404)  

  if error:
    return custom_response(error, 400)
  order = OrderModel(data)
  order.save()
  data = order_schema.dump(order).data
  return custom_response(data, 201)

@order_api.route('/', methods=['GET'])
def get_all():
  """
  Get All orders
  """
  orders = OrderModel.get_all_orders()
  data = order_schema.dump(orders, many=True).data
  return custom_response(data, 200)

@order_api.route('/<int:order_id>', methods=['GET'])
def get_one(order_id):
  """
  Get A order
  """
  order = OrderModel.get_one_order(order_id)
  if not order:
    return custom_response({'error': 'order not found'}, 404)
  data = order_schema.dump(order).data
  return custom_response(data, 200)

@order_api.route('/<int:order_id>', methods=['PUT'])
@Auth.auth_required
def update(order_id):
  """
  Update A order
  """
  req_data = request.get_json()
  order = OrderModel.get_one_order(order_id)
  if not order:
    return custom_response({'error': 'order not found'}, 404)
  data = order_schema.dump(order).data
  data, error = order_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)

  order.update(data)
  return custom_response(data, 200)

@order_api.route('/delete/<int:order_id>', methods=['DELETE'])
@Auth.auth_required
def delete(order_id):
  """
  Delete A order
  """
  order = OrderModel.get_one_order(order_id)
  if not order:
    return custom_response({'error': 'order not found'}, 404)
  data = order_schema.dump(order).data
  
  order.delete()
  return custom_response({'message': 'deleted'}, 204)
  

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )