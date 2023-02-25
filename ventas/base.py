import redis
import socket
from datetime import date, datetime, timedelta
import json
import jsonschema
from jsonschema import validate
from flask_restful import Resource
from flask import request
from flask import Flask  
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)
cors = CORS(app)
api = Api(app)

pool = redis.ConnectionPool(host='redis', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)

class VentaListResource(Resource):

    def valida_json(self,jsonData):
        try:
            json.loads(jsonData)
        except ValueError as err:
            return False
        return True
    
    def valida_estructura(self,jsonData):
        
        ventaSchema = {
            "type": "object",
            "properties": {
                "cliente": {"type": "string"},
                "clienteID": {"type": "number"},
                "direccion": {"type": "string"},
                "ciudad": {"type": "string"},
                "vendedor": {"type": "string"},
                "fechaPedido": {"type": "string"},
                "fechaEntrega": {"type": "string"},
                "metodoPago": {"type": "string"},
                "productos" : []
            },
        }
        try:
            validate(instance=jsonData, schema=ventaSchema)
        except jsonschema.exceptions.ValidationError as err:
            return False
        return True
    
    def valida_campos(self,orden):
        fecha = date.today()

        if  orden["cliente"] == "":
           orden["cliente"] = "Generico"
        if  orden["ciudad"] == "":
           orden["ciudad"] = "Bogota"
        if  orden["fechaPedido"] == "":
            orden["fechaPedido"] = fecha.strftime("%Y-%m-%d")
        if  orden["fechaEntrega"] == "":
            orden["fechaEntrega"] = (fecha + timedelta(days=3)).strftime("%Y-%m-%d")
        if  orden["metodoPago"] == "":
            orden["metodoPago"] = "Financiamiento"
        if  orden["vendedor"] == "":
            orden["vendedor"] = "Generico"
        return orden
    
    def post(self):
        # Validación de los campos de entrada y enmascaramiento

        orden_validada = {
            "cliente": request.json["cliente"],
            "clienteID": request.json["clienteID"],
            "direccion": request.json["direccion"],
            "vendedor": request.json["vendedor"],
            "ciudad": request.json["ciudad"],
            "fechaPedido": request.json["fechaPedido"],
            "fechaEntrega": request.json["fechaEntrega"],
            "metodoPago": request.json["metodoPago"],
            "productos": request.json["productos"]
        }
        
        hostIp = socket.gethostbyname(socket.gethostname())
        orden = self.valida_campos(orden_validada)
     
        # Enviamos la orden a la cola de Redis
        redis.rpush('ventas', json.dumps(orden))
        
        # Obenemos la ip del servidor que toma la petición
        response = {
            "HTTPCode": 200,
            "IP": hostIp,
        }

        return response


# Agregamos el recurso que expone la funcionalidad ventas
api.add_resource(VentaListResource, '/cpp/ventas')

api.init_app(app)
# Agregamos el recurso que expone la funcionalidad ventas
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
