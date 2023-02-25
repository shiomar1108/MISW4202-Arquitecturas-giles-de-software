import redis
import socket
from datetime import datetime, timezone,timedelta
import json
import jsonschema
from jsonschema import validate
from flask_restful import Resource
from flask import request
from flask import Flask  
from flask_cors import CORS
from flask_restful import Api
from modelos import db,Milog

            


class VentaListResource(Resource):

    def log(self,dato1,dato2):
        new_reg = Milog( 
                            data= dato1, 
                            description= dato2
                            )
        db.session.add(new_reg)
        db.session.commit()
            
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
    
    def valida_campos(self):
        
        orden = {
            "cliente": request.json["cliente"],
            "clienteID": request.json["clienteID"],
            "direccion": request.json["direccion"],
            "ciudad": request.json["ciudad"],
            "vendedor": request.json["vendedor"],
            "fechaPedido": "",
            "fechaEntrega": "",
            "metodoPago": request.json["metodoPago"],
            "productos": request.json["productos"]
        }
        
        
        diferencia = timedelta(hours=-5)   
        fecha_y_hora_actuales = datetime.now()
        zona_horaria = timezone(diferencia)
        fecha_y_hora_bogota = fecha_y_hora_actuales.astimezone(zona_horaria)
        fecha_y_hora_bogota_en_texto = fecha_y_hora_bogota.strftime('%Y-%m-%d')
        print(fecha_y_hora_bogota_en_texto)
        if  orden["cliente"] == "":
           orden["cliente"] = "Generico"
           self.log("cliente","Generico")
        
        if  orden["ciudad"] == "":
           orden["ciudad"] = "Bogota"
           self.log("ciudad","Bogota")

        if  orden["vendedor"] == "":
           orden["vendedor"] = "Generico"
           self.log("vendedor","Generico")
           
        print(orden["fechaPedido"])
        if  request.json["fechaPedido"] == "":
            orden["fechaPedido"] = fecha_y_hora_bogota_en_texto
            self.log("fechaPedido",fecha_y_hora_bogota_en_texto )
        else:
            orden["fechaPedido"] = str(datetime.strptime(request.json["fechaPedido"], '%Y-%m-%d').date())
           
        if  orden["fechaEntrega"] == "":
           orden["fechaEntrega"] = fecha_y_hora_bogota_en_texto
           self.log("fechaEntrega",fecha_y_hora_bogota_en_texto)
        else:
            orden["fechaEntrega"]  = str(datetime.strptime(request.json["fechaEntrega"], '%Y-%m-%d').date())
           
        if  orden["metodoPago"] == "":
           orden["metodoPago"] = "Efectivo"
           self.log("metodoPago","Efectivo")                                            
              
        return orden
    
    def post(self):
        # Validación de los campos de entrada y enmascaramiento
        orden = self.valida_campos()
     
        # Enviamos la orden a la cola de Redis
        redis.rpush('ventas', json.dumps(orden))
        
        # Obenemos la ip del servidor que toma la petición
        hostIp = socket.gethostbyname(socket.gethostname())
        response = {
            "HTTPCode": 200,
            "IP": hostIp,
        }

        return response



app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logCPP.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app_context = app.app_context()
app_context.push()
api = Api(app)

#pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
pool = redis.ConnectionPool(host='redis', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)


# Agregamos el recurso que expone la funcionalidad ventas
api.add_resource(VentaListResource, '/cpp/ventas')

db.init_app(app)
db.create_all()


# Agregamos el recurso que expone la funcionalidad ventas
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    



