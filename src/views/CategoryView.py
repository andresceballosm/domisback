from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.CategoryModel import CategoryModel, CategorySchema

category_api = Blueprint('category_api', __name__)
category_schema = CategorySchema()


@category_api.route('/create', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create Category Function
  """
  req_data = request.get_json()
  data, error = category_schema.load(req_data)
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

@category_api.route('/<int:category_id>', methods=['GET'])
def get_one(category_id):
  """
  Get A Category
  """
  category = CategoryModel.get_one_category(category_id)
  if not category:
    return custom_response({'error': 'category not found'}, 404)
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
    return custom_response({'error': 'category not found'}, 404)
  data = category_schema.dump(category).data
  
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
    return custom_response({'error': 'category not found'}, 404)
  data = category_schema.dump(category).data

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