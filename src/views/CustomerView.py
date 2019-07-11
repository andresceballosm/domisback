from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.CustomerModel import CustomerModel, CustomerSchema
from ..models.StoreModel import StoreModel, StoreSchema
from ..models.CategoryModel import CategoryModel, CategorySchema

customer_api = Blueprint('customer_api', __name__)
customer_schema = CustomerSchema()

@customer_api.route('/create', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create customer Function
  """
  req_data = request.get_json()
  req_data['user'] = g.user.get('id')
  data, error = customer_schema.load(req_data) 
  if error:
    return custom_response(error, 400)
  customer = CustomerModel(data)
  customer.save()
  data = customer_schema.dump(customer).data
  return custom_response(data, 201)

@customer_api.route('/', methods=['GET'])
def get_all():
  """
  Get All customers
  """
  customers = CustomerModel.get_all_customers()
  data = customer_schema.dump(customers, many=True).data
  return custom_response(data, 200)

@customer_api.route('/<int:customer_id>', methods=['GET'])
def get_one(customer_id):
  """
  Get A customer
  """
  customer = CustomerModel.get_one_customer(customer_id)
  if not customer:
    return custom_response({'error': 'customer not found'}, 404)
  data = customer_schema.dump(customer).data
  return custom_response(data, 200)

@customer_api.route('/<int:customer_id>', methods=['PUT'])
@Auth.auth_required
def update(customer_id):
  """
  Update A customer
  """
  req_data = request.get_json()
  customer = CustomerModel.get_one_customer(customer_id)
  if not customer:
    return custom_response({'error': 'customer not found'}, 404)
  data = customer_schema.dump(customer).data
  if data.get('user') != g.user.get('id'):
    return custom_response({'error': 'Permiso denegado'}, 400)
  data, error = customer_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  customer.update(data)
  
  data = customer_schema.dump(customer).data
  return custom_response(data, 200)

@customer_api.route('/delete/<int:customer_id>', methods=['DELETE'])
@Auth.auth_required
def delete(customer_id):
  """
  Delete A customer
  """
  customer = CustomerModel.get_one_customer(customer_id)
  if not customer:
    return custom_response({'error': 'customer not found'}, 404)
  data = customer_schema.dump(customer).data
  store_id = data.get('store_id')
  if store_id != g.user.get('id'):
    return custom_response({'error': 'Permiso Denegado'}, 400)
  if data.get('user') != g.user.get('id'):
    return custom_response({'error': 'Permiso denegado'}, 400)
  customer.delete()
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