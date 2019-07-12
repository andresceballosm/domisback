from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.AddressModel import AddressModel, AddressSchema
from ..models.StoreModel import StoreModel, StoreSchema
from ..models.CategoryModel import CategoryModel, CategorySchema

address_api = Blueprint('address_api', __name__)
address_schema = AddressSchema()

@address_api.route('/create', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create address Function
  """
  req_data = request.get_json()
  req_data['user'] = g.user.get('id')
  data, error = address_schema.load(req_data) 
  if error:
    return custom_response(error, 400)
  address = AddressModel(data)
  address.save()
  data = address_schema.dump(address).data
  return custom_response(data, 201)

@address_api.route('/', methods=['GET'])
def get_all():
  """
  Get All addresses
  """
  addresses = AddressModel.get_all_addresses()
  data = address_schema.dump(addresses, many=True).data
  return custom_response(data, 200)

@address_api.route('/<int:address_id>', methods=['GET'])
def get_one(address_id):
  """
  Get A address
  """
  address = AddressModel.get_one_address(address_id)
  if not address:
    return custom_response({'error': 'address not found'}, 404)
  data = address_schema.dump(address).data
  return custom_response(data, 200)

@address_api.route('/<int:address_id>', methods=['PUT'])
@Auth.auth_required
def update(address_id):
  """
  Update A address
  """
  req_data = request.get_json()
  address = AddressModel.get_one_address(address_id)
  if not address:
    return custom_response({'error': 'address not found'}, 404)
  data = address_schema.dump(address).data
  if data.get('user') != g.user.get('id'):
    return custom_response({'error': 'Permiso denegado'}, 400)
  data, error = address_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  address.update(data)
  
  data = address_schema.dump(address).data
  return custom_response(data, 200)

@address_api.route('/delete/<int:address_id>', methods=['DELETE'])
@Auth.auth_required
def delete(address_id):
  """
  Delete A address
  """
  address = AddressModel.get_one_address(address_id)
  if not address:
    return custom_response({'error': 'address not found'}, 404)
  data = address_schema.dump(address).data
  store_id = data.get('store_id')
  if store_id != g.user.get('id'):
    return custom_response({'error': 'Permiso Denegado'}, 400)
  if data.get('user') != g.user.get('id'):
    return custom_response({'error': 'Permiso denegado'}, 400)
  address.delete()
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