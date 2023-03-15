import requests
import socket
from flask_restful import Resource
from flask import request
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


class RutaClientes(Resource):
    @jwt_required()
    def get(self):
        headers = {'Authorization': request.headers['Authorization']}
        user = requests.get(f"http://localhost:5000/cpp/users/{request.json['user']}", headers=headers)
        hostIp = socket.gethostbyname(socket.gethostname())
        if user.status_code==200 and request.json['user'] == 1:
            response = {
                "HTTPCode": 200,
                "IP": hostIp,
                "user": request.json['user'],
                "RutaEntrega": {
                    "Cliente1": "Tienda de Pedro",
                    "Direccion1": "Santa Fe, Bogota",
                    "Cliente2": "Tienda de Juan",
                    "Direccion2": "Santa Teresa, Bogota",
                    "Cliente3": "Tienda de Felipe",
                    "Direccion3": "Kennedy, Bogota",
                    "Cliente4": "Tienda de Pedro",
                    "Direccion4": "Puente Aranda, Bogota",
                },
            }
        else:
            response = {
                "HTTPCode": 409,
                "IP": hostIp,
            }

        return response

app = Flask(__name__)
cors = CORS(app)
app.config["JWT_SECRET_KEY"] = "secret-jwt"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
jwt = JWTManager(app)


app_context = app.app_context()
app_context.push()
api = Api(app)

# Agregamos el recurso que expone la funcionalidad ventas
api.add_resource(RutaClientes, "/cpp/RutaClientes/")

# Agregamos el recurso que expone la funcionalidad ventas
if __name__ == "__main__":
    app.run(debug=True, host='localhost',port=8080)
