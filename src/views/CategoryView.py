from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.CategoryModel import CategoryModel, CategorySchema
from ..models.StoreModel import StoreModel, StoreSchema

category_api = Blueprint('category_api', __name__)
category_schema = CategorySchema()
store_schema = StoreSchema()

def validateStore(type):
  stores = StoreModel.get_all_stores()
  data = store_schema.dump(stores, many=True).data
  print('data',data)
  print('store', data)
  for store in data:
    if store['id'] == type:
        return True
  

@category_api.route('/create', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create Category Function
  """
  req_data = request.get_json()
  data, error = category_schema.load(req_data)
  storevalid = validateStore(data['store_id'])
  if storevalid == None:
    return custom_response({'error': 'store_id no existe!'}, 404)  
  if error:
    return custom_response(error, 400)
  category = CategoryModel(data)
  category.save()
  data = category_schema.dump(category).data
  return custom_response(data, 201)

@category_api.route('/', methods=['GET'])
def get_all():
  """
  Get All Categories
  """
  categories = CategoryModel.get_all_categories()
  data = category_schema.dump(categories, many=True).data
  return custom_response(data, 200)

@category_api.route('/store/<int:store_id>', methods=['GET'])
def get_by_store(store_id):
  """
  Get All Categories By Store
  """
  categories = CategoryModel.get_categories_by_store(store_id)
  if not categories:
    return custom_response({'error': 'No se encontraron categorias para este negocio.'}, 404)
  data = category_schema.dump(categories, many=True).data
  return custom_response(data, 200)

@category_api.route('/<int:category_id>', methods=['GET'])
def get_one(category_id):
  """
  Get A Category
  """
  category = CategoryModel.get_one_category(category_id)
  if not category:
    return custom_response({'error': 'Categoria no encontrada.'}, 404)
  data = category_schema.dump(category).data
  return custom_response(data, 200)

@category_api.route('/<int:category_id>', methods=['PUT'])
@Auth.auth_required
def update(category_id):
  """
  Update A Category
  """
  req_data = request.get_json()
  category = CategoryModel.get_one_category(category_id)
  if not category:
    return custom_response({'error': 'Categoria no encontrada.'}, 404)
  data = category_schema.dump(category).data
  store_id = data.get('store_id')
  if store_id != g.user.get('id'):
    return custom_response({'error': 'Permiso Denegado'}, 401)
  data, error = category_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  category.update(data)
  
  data = category_schema.dump(category).data
  return custom_response(data, 200)

@category_api.route('/delete/<int:category_id>', methods=['DELETE'])
@Auth.auth_required
def delete(category_id):
  """
  Delete A Category
  """
  category = CategoryModel.get_one_category(category_id)
  if not category:
    return custom_response({'error': 'Categoria no encontrada.'}, 404)
  data = category_schema.dump(category).data
  store_id = data.get('store_id')
  if store_id != g.user.get('id'):
    return custom_response({'error': 'Permiso Denegado'}, 401)
  
  category.delete()
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