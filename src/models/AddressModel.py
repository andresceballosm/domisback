from . import db
import datetime
from marshmallow import fields, Schema
from .StoreModel import  StoreModel
from .CategoryModel import CategoryModel
from .OrderModel import OrderModel, OrderSchema

class AddressModel(db.Model):
  """
  Address Model
  """

  __tablename__ = 'addresses'

  id = db.Column(db.Integer, primary_key=True)
  type_address = db.Column(db.String(128))  # CASA / OFICINA / APARTAMENTO
  address = db.Column(db.String(128), nullable=False)
  phone = db.Column(db.Integer, nullable=False)
  user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)

  def __init__(self, data):
    self.type_address = data.get('type_address')
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
  def get_all_addresses():
    return AddressModel.query.all()
  
  @staticmethod
  def get_one_address(id):
    return AddressModel.query.filter(AddressModel.user == id).first()
    # return AddressModel.query.get(id)

  def __repr__(self):
    return '<id {}>'.format(self.id)

class AddressSchema(Schema):
  id = fields.Int(dump_only=True)
  type_address = fields.Str(required=False)
  address = fields.Str(required=True)
  phone = fields.Int(required=True)
  user = fields.Int(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  #orders = fields.Nested(OrderSchema, many=True)