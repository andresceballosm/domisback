from . import db
import datetime
from marshmallow import fields, Schema
import uuid
from .StoretypeModel import StoretypeModel, StoretypeSchema
from .CategoryModel import CategorySchema

def generate_id():
    return str(uuid.uuid4()).split("-")[-1]
  
class StoreModel(db.Model):
  """
  Store Model
  """

  __tablename__ = 'stores'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  country = db.Column(db.Text, nullable=False)
  region = db.Column(db.Text, nullable=False)
  city = db.Column(db.Text, nullable=False)
  address = db.Column(db.Text, nullable=False)
  storetype = db.Column(db.Integer, nullable=False)
  perimeter = db.Column(db.Integer, nullable=False)
  latitude = db.Column(db.Float, nullable=False)
  longitude = db.Column(db.Float, nullable=False)
  license = db.Column(db.Boolean, default=False)
  active = db.Column(db.Boolean, default=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)
  owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

  def __init__(self, data):
    self.name = data.get('name')
    self.country = data.get('country')
    self.region = data.get('region')
    self.city = data.get('city')
    self.address = data.get('address')
    self.storetype = data.get('storetype')
    self.perimeter = data.get('perimeter')
    self.latitude = data.get('latitude')
    self.longitude = data.get('longitude')
    self.license = data.get('license')
    self.active = data.get('active')
    self.owner_id = data.get('owner_id')
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()


  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      setattr(self, key, item)
    self.modified_at = datetime.datetime.utcnow()
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  @staticmethod
  def get_all_stores():
    return StoreModel.query.all()
  
  @staticmethod
  def get_one_store(id):
    return StoreModel.query.get(id)
  
  @staticmethod
  def get_store_by_storetype(storetype, city):
    return StoreModel.query.filter(StoreModel.storetype == storetype, StoreModel.city == city).all()


  def __repr__(self):
    return '<id {}>'.format(self.id)

class StoreSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  country = fields.Str(required=True)
  region = fields.Str(required=True)
  city = fields.Str(required=True)
  address = fields.Str(required=True)
  storetype = fields.Int(required=True)
  perimeter = fields.Int(required=True)
  latitude = fields.Float(required=True)
  longitude = fields.Float(required=True)
  license = fields.Boolean(required=False)
  active = fields.Boolean(required=False)
  owner_id = fields.Int(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  categories = fields.Nested(CategorySchema, many=True)