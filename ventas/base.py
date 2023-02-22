from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from redis import Redis
from rq import Queue

app = Flask(__name__)
ma = Marshmallow(app)
cors = CORS(app)
api = Api(app)

q = Queue(connection=Redis(host='redis', port=6379, db=0))


