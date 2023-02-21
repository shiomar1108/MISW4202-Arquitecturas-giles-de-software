from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
import requests
from redis import Redis
from rq import Queue


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/registroVentas.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
q = Queue(connection=Redis(host='redis', port=6379, db=0))



def process_venta(venta_id):
    print('Se procesa venta')
