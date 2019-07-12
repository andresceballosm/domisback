from . import db
import datetime
from marshmallow import fields, Schema
from .StoreModel import  StoreModel
from .CategoryModel import CategoryModel

class ProductModel(db.Model):
  """
  Product Model
  """

  __tablename__ = 'products'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  price = db.Column(db.Float, nullable=False)
  money = db.Column(db.String(128), nullable=False)
  brand = db.Column(db.String(128), nullable=False)
  quantity = db.Column(db.Float, nullable=False)
  unity = db.Column(db.String(128), nullable=False)
  description = db.Column(db.String(128), nullable=False)
  store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
  category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
  image = db.Column(db.String(128), nullable=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)

  def __init__(self, data):
    self.name = data.get('name')
    self.money = data.get('money')
    self.brand = data.get('brand')
    self.price = data.get('price')
    self.quantity = data.get('quantity')
    self.unity = data.get('unity')
    self.description = data.get('description')
    self.store_id = data.get('store_id')
    self.category_id = data.get('category_id')
    self.image = data.get('image')
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
  def get_products_by_category(category_id):
    return ProductModel.query.filter(ProductModel.category_id == category_id).all()
  
  @staticmethod
  def get_one_product(id):
    return ProductModel.query.get(id)

  def __repr__(self):
    return '<id {}>'.format(self.id)

class ProductSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  money = fields.Str(required=True)
  brand = fields.Str(required=True)
  price = fields.Float(required=True)
  quantity = fields.Float(required=True)
  unity = fields.String(required=True)
  description = fields.Str(required=True)
  store_id = fields.Int(required=True)
  category_id = fields.Int(required=True)
  image = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)