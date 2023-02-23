from base import app, api,  q
import socket
from flask_restful import Resource
from flask import request

class RegistroVentaResource(Resource):
    def get(self):
       
        hostIp = socket.gethostbyname(socket.gethostname())
        sub = q.pubsub()
        q.publish('ventas', "mi mugre")
        # Enviamos la orden a la cola de Redis
        
        
        sub.subscribe("ventas")
        
        
        msg = sub.get_message()
        print(msg)

        cola = q.pubsub()
        # subscribe to classical music
        cola.subscribe('ventas')
        datos = cola.get_message()
        print(datos)
        # now bob can find alice’s music by simply using get_message()
        #datos = cola.get_message()['data']
        #print(datos)
        
        # Obenemos la ip del servidor que toma la petición
        
        response = {
            "HTTPCode": 200,
            "IP": hostIp,
        }

        return response


# Agregamos el recurso que expone la funcionalidad ventas
api.add_resource(RegistroVentaResource, '/cpp/registro')

api.init_app(app)
# Agregamos el recurso que expone la funcionalidad ventas
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=6000)


