from . import db
import datetime
from marshmallow import fields, Schema
from .StoreModel import  StoreModel
from .CategoryModel import CategoryModel

class OrderModel(db.Model):
  """
  Order Model
  """

  __tablename__ = 'orders'

  id = db.Column(db.Integer, primary_key=True)
  user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
  total = db.Column(db.Float, nullable=False)
  status = db.Column(db.String, nullable=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)

  def __init__(self, data):
    self.user = data.get('user')
    self.store_id = data.get('store_id')
    self.total = data.get('total')
    self.status = data.get('status')
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
  def get_all_orders():
    return OrderModel.query.all()

  # @staticmethod
  # def get_order(order_number):
  #   return OrderModel.query.filter(OrderModel.order_number == order_number).all()
  
  @staticmethod
  def get_one_order(id):
    return OrderModel.query.get(id)

  def __repr__(self):
    return '<id {}>'.format(self.id)

class OrderSchema(Schema):
  id = fields.Int(dump_only=True)
  user = fields.Int(required=True)
  store_id = fields.Int(required=True)
  total = fields.Float(required=True)
  status = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)