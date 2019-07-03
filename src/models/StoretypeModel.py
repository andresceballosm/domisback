from . import db
import datetime
from marshmallow import fields, Schema
from .StoreModel import StoreSchema

class StoretypeModel(db.Model):
  """
  Store Model
  """

  __tablename__ = 'storetype'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)

  def __init__(self, data):
    self.name = data.get('name')
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
    return StoretypeModel.query.all()
  
  @staticmethod
  def get_one_store(id):
    return StoretypeModel.query.get(id)

  def __repr__(self):
    return '<id {}>'.format(self.id)

class StoretypeSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  stores = fields.Nested(StoreSchema, many=True)