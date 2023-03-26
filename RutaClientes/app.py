import requests
import socket
from flask_restful import Resource
from flask import request
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager, jwt_required, decode_token


class RutaClientes(Resource):
    # @jwt_required()
    def get(self, user_id):
        jwt = request.headers['jwt']
        decodedToken = decode_token(jwt)
        headers = {'Authorization': request.headers['Authorization']}
        user = requests.get(
            f"http://mcs_usuario:5000/cpp/users/{user_id}", headers=headers)
        print(user)
        hostIp = socket.gethostbyname(socket.gethostname())
        print(user.json()['rol'])
        print(user.json()['id'])
        if user.json()['rol'] == 'REP':
            if user.status_code == 200 and user_id == user.json()['id']:
                response = {
                    "HTTPCode": 200,
                    "IP": hostIp,
                    "user": user_id,
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
                    "decode_token": str(decodedToken['sub'])
                }
                return response, 200
            else:
                response = {
                    "HTTPCode": 409,
                    "Mensaje": "No eres el usuario correcto",
                    "IP": hostIp,
                }
                return response, 409
        else:
            response = {
                "HTTPCode": 409,
                "Mensaje": "No tienes el rol correcto",
                "IP": hostIp,
            }
            return response, 409


app = Flask(__name__)
cors = CORS(app)
app.config["JWT_SECRET_KEY"] = "JwBGj2B4XFAKhYmn8Pgk0vH2w7UvgYfXAJ32e5rs8vI="
jwt = JWTManager(app)
app_context = app.app_context()
app_context.push()
api = Api(app)

# Agregamos el recurso que expone la funcionalidad ventas
api.add_resource(RutaClientes, "/cpp/ruta/clientes/<int:user_id>")

# Agregamos el recurso que expone la funcionalidad ventas
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
