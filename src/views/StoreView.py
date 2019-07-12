from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.UserModel import UserModel, UserSchema
from ..models.StoreModel import StoreModel, StoreSchema
from ..models.StoretypeModel import StoretypeModel, StoretypeSchema
from ..utils.distance import DistanceModel

store_api = Blueprint('store_api', __name__)
store_schema = StoreSchema()
user_schema = UserSchema()
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
  userAuth = UserModel.get_one_user(req_data['owner_id'])
  user = user_schema.dump(userAuth).data

  if user['type_user'] == 'client':
    return custom_response({'error': 'No tiene los privilegios de usuario para crear un negocio!'}, 401)  

  data, error = store_schema.load(req_data)
  storetypevalid = validateStoretype(data['storetype'])
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
    return custom_response({'info': 'No se encontraron negocios'}, 204)
  data = store_schema.dump(store).data
  return custom_response(data, 200)

@store_api.route('/locations', methods=['POST'])
def get_all_storetype():
  """
  Get A Store by Storetype and city
  """
  req_data = request.get_json()
  storetype = req_data['storetype']
  city = req_data['city']
  location = req_data['location']
  lat = location['latitude']
  lng = location['longitude']
  stores= []
  allStores = StoreModel.get_store_by_storetype(storetype,city)
  data = store_schema.dump(allStores, many=True).data

  if not allStores:
    return custom_response({'info': 'No se encontraron negocios'}, 204)

  for store in data:
    print('store[license]',store['license'])
    distance = DistanceModel.distance_cal(lat,lng,store['latitude'],store['longitude'])
    if store['license'] != False and store['active'] != False and distance <= store['perimeter']:
      stores.append(store)

  if not stores:
    return custom_response({'info': 'No se encontraron negocios en el perímetro.'}, 204)
  
  return custom_response(stores, 200)

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

  #Trae datos del usuario para validar si es admin
  userData = UserModel.get_one_user(g.user.get('id'))
  user = user_schema.dump(userData).data

  if data.get('owner_id') != g.user.get('id') and user['type_user'] != 'admin':
    return custom_response({'error': 'Permiso denegado'}, 401)
  
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

  #Trae datos del usuario para validar si es admin
  userData = UserModel.get_one_user(g.user.get('id'))
  user = user_schema.dump(userData).data

  if data.get('owner_id') != g.user.get('id') and user['type_user'] != 'admin':
    return custom_response({'error': 'Permiso denegado'}, 401)

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