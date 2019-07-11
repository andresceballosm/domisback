from . import db
import datetime
from marshmallow import fields, Schema
from .StoreModel import  StoreModel
from .CategoryModel import CategoryModel
from .OrderModel import OrderModel, OrderSchema

class CustomerModel(db.Model):
  """
  Customer Model
  """

  __tablename__ = 'customers'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  country = db.Column(db.String(128), nullable=False)
  region = db.Column(db.String(128), nullable=False)
  city = db.Column(db.String(128), nullable=False)
  region = db.Column(db.String(128), nullable=False)
  address = db.Column(db.String(128), nullable=False)
  phone = db.Column(db.Integer, nullable=False)
  user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)

  def __init__(self, data):
    self.name = data.get('name')
    self.country = data.get('country')
    self.region = data.get('region')
    self.city = data.get('city')
    self.address = data.get('address')
    self.phone = data.get('phone')
    self.user = data.get('user')
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
  def get_all_customers():
    return CustomerModel.query.all()
  
  @staticmethod
  def get_one_customer(id):
    return CustomerModel.query.get(id)

  def __repr__(self):
    return '<id {}>'.format(self.id)

class CustomerSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  country = fields.Str(required=True)
  region = fields.Str(required=True)
  city = fields.Str(required=True)
  address = fields.Str(required=True)
  phone = fields.Int(required=True)
  user = fields.Int(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  orders = fields.Nested(OrderSchema, many=True)