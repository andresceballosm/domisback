from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.StoreModel import StoreModel, StoreSchema
from ..models.StoretypeModel import StoretypeModel, StoretypeSchema
from ..utils.distance import DistanceModel

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
    return custom_response({'error': 'No se encontraron negocios'}, 404)
  data = store_schema.dump(store).data
  return custom_response(data, 200)

@store_api.route('storetype/<int:storetype>/<city>', methods=['GET'])
def get_all_storetype(storetype,city):
  """
  Get A Store by Storetype and city
  """
  lat=4.726885
  lng= -74.048243
  storesData = [
    {
        "active": 'false',
        "address": "Calle 159",
        "city": "Bogota",
        "country": "Colombia",
        "created_at": "2019-07-11T16:29:28.137590+00:00",
        "id": 1,
        "latitude": 4.735909,
        "license": 'false',
        "longitude": -74.032106,
        "modified_at": "2019-07-11T16:29:28.137608+00:00",
        "name": "Cigarreria Madgala",
        "owner_id": 2,
        "region": "Cundinamarca",
        "storetype": 1
    },
    {
        "active": 'false',
        "address": "Calle 161",
        "city": "Bogota",
        "country": "Colombia",
        "created_at": "2019-07-11T18:55:55.393171+00:00",
        "id": 2,
        "latitude": 4.740186, 
        "license": 'false',
        "longitude": -74.057041,
        "modified_at": "2019-07-11T18:55:55.393189+00:00",
        "name": "Cigarreria La Quinta",
        "owner_id": 2,
        "region": "Cundinamarca",
        "storetype": 1
    }
  ]

  for stor in storesData:
    distance = DistanceModel.distance_cal(lat,lng,stor['latitude'],stor['longitude'])
    print('distance ==', distance)

  stores = StoreModel.get_store_by_storetype(storetype,city)
  if not stores:
    return custom_response({'error': 'No se encontraron negocios'}, 404)
  data = store_schema.dump(stores, many=True).data
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