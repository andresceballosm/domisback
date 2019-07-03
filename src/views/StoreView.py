from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.StoreModel import StoreModel, StoreSchema
from ..models.StoretypeModel import StoretypeModel, StoretypeSchema

store_api = Blueprint('store_api', __name__)
store_schema = StoreSchema()
storetype_schema = StoretypeSchema()

def validateStoretype(type):
  storetypes = StoretypeModel.get_all_stores()
  data = storetype_schema.dump(storetypes, many=True).data
  print('storestype', data)
  for storetype in data:
    if storetype['id'] == type:
        return True
  
      
@store_api.route('/create', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create Store Function
  """
  req_data = request.get_json()
  req_data['owner_id'] = g.user.get('id')
  data, error = store_schema.load(req_data)
  # print(data['storetype'])
  storetypevalid = validateStoretype(data['storetype'])
  print('is valid',storetypevalid)
  if storetypevalid == None:
    return custom_response({'error': 'storetype no existe!'}, 404)  
   
  if error:
    return custom_response(error, 400)
  store = StoreModel(data)
  store.save()
  data = store_schema.dump(store).data
  return custom_response(data, 201)

@store_api.route('/', methods=['GET'])
def get_all():
  """
  Get All Stores
  """
  stores = StoreModel.get_all_stores()
  data = store_schema.dump(stores, many=True).data
  return custom_response(data, 200)

@store_api.route('/<int:store_id>', methods=['GET'])
def get_one(store_id):
  """
  Get A Store
  """
  store = StoreModel.get_one_store(store_id)
  if not store:
    return custom_response({'error': 'post not found'}, 404)
  data = store_schema.dump(store).data
  return custom_response(data, 200)

@store_api.route('/<int:store_id>', methods=['PUT'])
@Auth.auth_required
def update(store_id):
  """
  Update A Store
  """
  req_data = request.get_json()
  store = StoreModel.get_one_store(store_id)
  if not store:
    return custom_response({'error': 'store not found'}, 404)
  data = store_schema.dump(store).data
  if data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permission denied'}, 400)
  
  data, error = store_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  store.update(data)
  
  data = store_schema.dump(store).data
  return custom_response(data, 200)

@store_api.route('/delete/<int:store_id>', methods=['DELETE'])
@Auth.auth_required
def delete(store_id):
  """
  Delete A Store
  """
  store = StoreModel.get_one_store(store_id)
  if not store:
    return custom_response({'error': 'store not found'}, 404)
  data = store_schema.dump(store).data
  if data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permission denied'}, 400)

  store.delete()
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