from base import app, api, ma, q, Resource, Flask, request
import socket
from datetime import datetime
import json
import jsonschema
from jsonschema import validate
from sender import send_venta


class VentaListResource(Resource):

    def valida_json(jsonData):
        try:
            json.loads(jsonData)
        except ValueError as err:
            return False
        return True
    
    def valida_estructura(jsonData):
        
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
                
            },
        }
        try:
            validate(instance=jsonData, schema=ventaSchema)
        except jsonschema.exceptions.ValidationError as err:
            return False
        return True
    
    def valida_campos(self):
        return False
    
    def post(self):
        # Validación de los campos de entrada y enmascaramiento
        orden_validada = {
            "cliente": request.json["cliente"],
            "clienteID": request.json["clienteID"],
            "direccion": request.json["direccion"],
            "ciudad": request.json["ciudad"],
            "fechaPedido": str(datetime.strptime(request.json["fechaPedido"], '%Y-%m-%d').date()),
            "fechaEntrega": str(datetime.strptime(request.json["fechaEntrega"], '%Y-%m-%d').date()),
            "metodoPago": request.json["metodoPago"],
            "productos": request.json["productos"]
        }
        hostIp = socket.gethostbyname(socket.gethostname())
        if self.valida_json(request.json) == False:
            response = {
                "HTTPCode": 404,
                "IP": hostIp,
            }

            return response
        
        if self.valida_estructura(request.json) == False:
            response = {
                "HTTPCode": 404,
                "IP": hostIp,
            }

            return response
 
        # Enviamos la orden a la cola de Redis
        q.enqueue(send_venta, orden_validada)
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
