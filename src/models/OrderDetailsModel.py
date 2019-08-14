from . import db
import datetime
from marshmallow import fields, Schema
from .StoreModel import  StoreModel
from .CategoryModel import CategoryModel

class OrderDetailsModel(db.Model):
  """
  Order Details Model
  """

  __tablename__ = 'orderDetails'

  id = db.Column(db.Integer, primary_key=True)
  order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
  category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
  product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
  price = db.Column(db.Float, nullable=False )
  quantity = db.Column(db.Float, nullable=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)

  def __init__(self, data):
    self.order_id = data.get('order_id')
    self.category_id = data.get('category_id')
    self.product_id = data.get('product_id')
    self.price = data.get('price')
    self.quantity = data.get('quantity')
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
  def get_all_ordersDetails():
    return OrderDetailsModel.query.all()

  @staticmethod
  def get_order_details(order_id):
    print('order_id',order_id)
    return OrderDetailsModel.query.filter(OrderDetailsModel.order_id == order_id).all()
  
  @staticmethod
  def get_one_orderDetail(id):
    return OrderDetailsModel.query.get(id)

  def __repr__(self):
    return '<id {}>'.format(self.id)

class OrderDetailsSchema(Schema):
  id = fields.Int(dump_only=True)
  order_id = fields.Int(required=True)
  category_id = fields.Int(required=True)
  product_id = fields.Int(required=True)
  price = fields.Float(required=True)
  quantity = fields.Float(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)