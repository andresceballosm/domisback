from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.StoretypeModel import StoretypeModel, StoretypeSchema

storetype_api = Blueprint('storetype_api', __name__)
storetype_schema = StoretypeSchema()


@storetype_api.route('/create', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create Store Function
  """
  req_data = request.get_json()
  data, error = storetype_schema.load(req_data)
  if error:
    return custom_response(error, 400)
  post = StoretypeModel(data)
  post.save()
  data = storetype_schema.dump(post).data
  return custom_response(data, 201)

@storetype_api.route('/', methods=['GET'])
def get_all():
  """
  Get All Storetypes
  """
  storetypes = StoretypeModel.get_all_stores()
  data = storetype_schema.dump(storetypes, many=True).data
  return custom_response(data, 200)

@storetype_api.route('/<int:storetype_id>', methods=['GET'])
def get_one(storetype_id):
  """
  Get A Store
  """
  post = StoretypeModel.get_one_store(storetype_id)
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = storetype_schema.dump(post).data
  return custom_response(data, 200)

@storetype_api.route('/<int:storetype_id>', methods=['PUT'])
@Auth.auth_required
def update(storetype_id):
  """
  Update A Store
  """
  req_data = request.get_json()
  post = StoretypeModel.get_one_store(storetype_id)
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = storetype_schema.dump(post).data
  
  data, error = storetype_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  post.update(data)
  
  data = storetype_schema.dump(post).data
  return custom_response(data, 200)

@storetype_api.route('/delete/<int:storetype_id>', methods=['DELETE'])
@Auth.auth_required
def delete(storetype_id):
  """
  Delete A Store
  """
  post = StoretypeModel.get_one_store(storetype_id)
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = storetype_schema.dump(post).data

  post.delete()
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