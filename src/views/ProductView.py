from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.ProductModel import ProductModel, ProductSchema
from ..models.StoreModel import StoreModel, StoreSchema
from ..models.CategoryModel import CategoryModel, CategorySchema

product_api = Blueprint('product_api', __name__)
product_schema = ProductSchema()
store_schema = StoreSchema()
category_schema = CategorySchema()

def validateStore(type):
  stores = StoreModel.get_all_stores()
  data = store_schema.dump(stores, many=True).data
  for store in data:
    if store['id'] == type:
        return True
  
def validateCategory(type):
  categories = CategoryModel.get_all_categories()
  data = category_schema.dump(categories, many=True).data
  for category in data:
    if category['id'] == type:
        return True

@product_api.route('/create', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create product Function
  """
  req_data = request.get_json()
  data, error = product_schema.load(req_data)
  storevalid = validateStore(data['store_id'])
  categoryvalid = validateCategory(data['category_id'])
  if storevalid == None:
    return custom_response({'error': 'store_id no existe!'}, 404)  
  if categoryvalid == None:
    return custom_response({'error': 'category_id no existe!'}, 404)  
  if error:
    return custom_response(error, 400)
  product = ProductModel(data)
  product.save()
  data = product_schema.dump(product).data
  return custom_response(data, 201)

@product_api.route('/', methods=['GET'])
def get_all():
  """
  Get All Products
  """
  products = ProductModel.get_all_products()
  data = product_schema.dump(products, many=True).data
  return custom_response(data, 200)

@product_api.route('/category/<int:category_id>', methods=['GET'])
def get_by_category(category_id):
  """
  Get All Products by category
  """
  products = ProductModel.get_products_by_category(category_id)
  if not products:
    return custom_response({'info': 'No se encontraron productos para esta categoria'}, 404)
  data = product_schema.dump(products, many=True).data
  return custom_response(data, 200)

@product_api.route('/<int:product_id>', methods=['GET'])
def get_one(product_id):
  """
  Get A product
  """
  product = ProductModel.get_one_product(product_id)
  if not product:
    return custom_response({'error': 'Producto no encontrado'}, 404)
  data = product_schema.dump(product).data
  return custom_response(data, 200)

@product_api.route('/<int:product_id>', methods=['PUT'])
@Auth.auth_required
def update(product_id):
  """
  Update A product
  """
  req_data = request.get_json()
  product = ProductModel.get_one_product(product_id)
  if not product:
    return custom_response({'error': 'Producto no encontrado'}, 404)
  data = product_schema.dump(product).data
  store_id = data.get('store_id')
  if store_id != g.user.get('id'):
    return custom_response({'error': 'Permiso Denegado'}, 401)
  data, error = product_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  product.update(data)
  
  data = product_schema.dump(product).data
  return custom_response(data, 200)

@product_api.route('/delete/<int:product_id>', methods=['DELETE'])
@Auth.auth_required
def delete(product_id):
  """
  Delete A product
  """
  product = ProductModel.get_one_product(product_id)
  if not product:
    return custom_response({'error': 'Producto no encontrado'}, 404)
  data = product_schema.dump(product).data
  store_id = data.get('store_id')
  if store_id != g.user.get('id'):
    return custom_response({'error': 'Permiso Denegado'}, 401)
  
  product.delete()
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