from flask import Flask  
from flask_cors import CORS
from flask_restful import Api
from redis import Redis

app = Flask(__name__)
cors = CORS(app)
api = Api(app)
q = Redis(host='redis', port=6379, db=0)
#q = Redis(host='localhost', port=6379, db=0)




