from . import db
import datetime
from marshmallow import fields, Schema
from .StoreModel import StoreModel

class CategoryModel(db.Model):
  """
  Category Model
  """

  __tablename__ = 'categories'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)
  store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
  

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
  def get_all_categories():
    return CategoryModel.query.all()
  
  @staticmethod
  def get_one_category(id):
    return CategoryModel.query.get(id)

  def __repr__(self):
    return '<id {}>'.format(self.id)

class CategorySchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  store_id = fields.Int(dump_only=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)