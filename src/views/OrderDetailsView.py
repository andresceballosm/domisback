from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.OrderModel import OrderModel, OrderSchema
from ..models.OrderDetailsModel import OrderDetailsModel, OrderDetailsSchema

from ..models.UserModel import UserModel, UserSchema
from ..models.CategoryModel import CategoryModel, CategorySchema
from ..models.ProductModel import ProductModel, ProductSchema

orderDetails_api = Blueprint('orderdetails_api', __name__)

order_schema = OrderSchema()
orderDetails_schema = OrderDetailsSchema()

user_schema = UserSchema()
category_schema = CategorySchema()
product_schema = ProductSchema()

def validateOrder(order_id):
  orders = OrderModel.get_one_order(order_id)
  data = order_schema.dump(orders).data
  if data['id'] == order_id:
    return True

def validateCategory(category_id):
  categories = CategoryModel.get_one_category(category_id)
  data = category_schema.dump(categories).data
  print('category ===', data)
  if data != {}:
   return True
    
def validateProduct(product_id):
  print('type product', product_id)
  products = ProductModel.get_one_product(product_id)
  data = product_schema.dump(products).data
  if data != {}:
   return True
      
def validateprice(product_id, price):  
  products = ProductModel.get_one_product(product_id)
  data = product_schema.dump(products).data
  if data['price'] == price:
   return True

@orderDetails_api.route('/create', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create order Detail Function
  """
  req_data = request.get_json()
  data, error = orderDetails_schema.load(req_data)
  ordervalid = validateOrder(data['order_id'])
  categoryvalid = validateCategory(data['category_id'])
  productvalid = validateProduct(data['product_id'])

  print('categoryvalid ==', categoryvalid)
  if ordervalid == None:
    return custom_response({'error': 'order_id no existe!'}, 404)  
  if categoryvalid == None:
    return custom_response({'error': 'category_id no existe!'}, 404)  
  if productvalid == None:
    return custom_response({'error': 'product_id no existe!'}, 404) 
  else:
    productpricevalid = validateprice(data['product_id'], data['price'])  
    if productpricevalid == None:
        return custom_response({'error': 'el precio del producto no es correcto!'}, 404) 

  if error:
    return custom_response(error, 400)
  orderDetail = OrderDetailsModel(data)
  orderDetail.save()
  data = orderDetails_schema.dump(orderDetail).data
  return custom_response(data, 201)

@orderDetails_api.route('/', methods=['GET'])
def get_all():
  """
  Get All orders details
  """
  ordersDetails = OrderDetailsModel.get_all_ordersDetails()
  data = orderDetails_schema.dump(ordersDetails, many=True).data
  return custom_response(data, 200)

@orderDetails_api.route('/order/<int:order_id>', methods=['GET'])
@Auth.auth_required
def get_order_details(order_id):
  """
  Get details by order_id
  """
  orderDetails = OrderDetailsModel.get_order_details(order_id)
  if not orderDetails:
    return custom_response({'error': 'order detail not found'}, 404)
  data = orderDetails_schema.dump(orderDetails, many=True).data
  return custom_response(data, 200)

@orderDetails_api.route('/<int:order_id>', methods=['GET'])
def get_one(order_id):
  """
  Get A order
  """
  order = OrderModel.get_one_order(order_id)
  if not order:
    return custom_response({'error': 'order not found'}, 404)
  data = order_schema.dump(order).data
  return custom_response(data, 200)

@orderDetails_api.route('/<int:order_id>', methods=['PUT'])
@Auth.auth_required
def update(orderDetail_id):
  """
  Update A order Detail
  """
  req_data = request.get_json()
  orderDetails = OrderDetailsModel.get_one_orderDetail(orderDetail_id)
  if not orderDetails:
    return custom_response({'error': 'order detail not found'}, 404)

  if g.user.get('type_user') != 'owner':
    return custom_response({'error': 'Permiso Denegado'}, 400)

  data = orderDetails_schema.dump(orderDetails).data
  data, error = orderDetails_schema.load(req_data, partial=True)

  if error:
    return custom_response(error, 400)
  orderDetails.update(data)

  return custom_response(data, 200)

@orderDetails_api.route('/delete/<int:order_id>', methods=['DELETE'])
@Auth.auth_required
def delete(order_id):
  """
  Delete A order Detail
  """
  orderDetail = OrderDetailsModel.get_one_orderDetail(order_id)
  if not orderDetail:
    return custom_response({'error': 'order not found'}, 404)
  data = orderDetails_schema.dump(orderDetail).data
  orderDetail.delete()
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