from . import db
import datetime
from marshmallow import fields, Schema
from .StoreModel import  StoreModel

class ProductModel(db.Model):
  """
  Product Model
  """

  __tablename__ = 'products'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
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
  def get_all_products():
    return ProductModel.query.all()
  
  @staticmethod
  def get_one_product(id):
    return ProductModel.query.get(id)

  def __repr__(self):
    return '<id {}>'.format(self.id)

class ProductSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  store_id = fields.Int(dump_only=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)