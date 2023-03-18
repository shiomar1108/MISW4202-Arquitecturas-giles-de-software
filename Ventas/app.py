import json
import sys
import traceback
from flask_restful import Resource
from flask import request
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
import pika
from cryptography.fernet import Fernet
from jproperties import Properties
from datetime import datetime
from flask_jwt_extended import JWTManager, jwt_required


# Function to registry log
def registry_log(file, severity, request, response):
    with open(file, 'a') as file:
        file.write(f"[{severity}]-[{datetime.now()}]-[request=>{request}]-[response=>{response}]\n")

# Function to read key
def load_security_key(key):
    return open(key, "rb").read()

# Function to decrypt key
def decrypt(key_to_decrypt):
    try:
        security_key = load_security_key('security.key')
        decrypt = Fernet(security_key)
        decryptedValue = decrypt.decrypt(key_to_decrypt)
        return decryptedValue
    except Exception as e:
        traceback.print_exc()

# Function to read property decrypted
def read_property(properti):
    try:
        configs = Properties()
        with open('app-config.properties', 'rb') as config_file:
            configs.load(config_file)
        return decrypt(configs[properti].data)
    except Exception as e:
        traceback.print_exc()
        raise Exception(str(e))


# Function to send message to queue
def send_message(host, vhost, user, password, queue, message):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, virtual_host=vhost,
                                      credentials=pika.PlainCredentials(user, password)))
        channel = connection.channel()
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
            ))
        connection.close()
    except pika.exceptions.ConnectionClosedByBroker as peccbb:
        traceback.print_exc()
        raise Exception(str(peccbb))
    except pika.exceptions.AMQPChannelError as peache:
        traceback.print_exc()
        raise Exception(str(peache))
    except pika.exceptions.AMQPConnectionError as peace:
        traceback.print_exc()
        raise Exception(str(peace))
    except Exception as e:
        traceback.print_exc()
        raise Exception(str(e))


# Clase con la logica de negocio
class RegistrarOrdenResource(Resource):

    #@jwt_required()
    def post(self):
        response = None
        try:
            # Se obtiene el request
            orden = request.json
            # Se obtienen las configuraciones de rabbitmq
            rabbit_host = read_property('HOST_RABBIT').decode()
            virtual_host = read_property('VIRTUAL_HOST_POST').decode()
            rabbit_user = read_property('USER_QUEUE_POST').decode()
            rabbit_password = read_property('PASSWORD_QUEUE_POST').decode()
            queue = read_property('QUEUE_POST').decode()
            send_message(host=rabbit_host, vhost=virtual_host, user=rabbit_user, password=rabbit_password,
                         queue=queue, message=orden)
            # Retornamos respuesta exitosa
            response = {
                "msg": "La orden sera procesada para registro",
                "orden": orden
            }
            registry_log('log_transactions_post.txt', 'SUCCESS',
                         json.dumps(orden), json.dumps(response))
            return response
        except Exception as e:
            traceback.print_exc()
            # Retornamos respuesta de error
            response = {
                "msg": str(e)
            }
            registry_log('log_transactions_post.txt', 'ERROR',
                         json.dumps(orden), json.dumps(response))
            return response, 500
        
class ActualizarOrdenResource(Resource):
    #@jwt_required()
    def put(self, orden_id):
        try:
            # Se obtiene el request
            orden = request.json
            orden['id'] = orden_id
            # Se obtienen las configuraciones de rabbitmq
            rabbit_host = read_property('HOST_RABBIT').decode()
            virtual_host = read_property('VIRTUAL_HOST_PUT').decode()
            rabbit_user = read_property('USER_QUEUE_PUT').decode()
            rabbit_password = read_property('PASSWORD_QUEUE_PUT').decode()
            queue = read_property('QUEUE_PUT').decode()
            send_message(host=rabbit_host, vhost=virtual_host, user=rabbit_user, password=rabbit_password,
                         queue=queue, message=orden)
            # Retornamos respuesta
            response = {
                "msg": f"La orden [{orden_id}] sera procesada para actualización",
                "orden": orden
            }
            registry_log('log_transactions_put.txt', 'SUCCESS',
                         json.dumps(orden), json.dumps(response))
            return response
        except Exception as e:
            traceback.print_exc()
            # Retornamos respuesta de error
            response = {
                "msg": str(e)
            }
            registry_log('log_transactions_put.txt', 'ERROR',
                         json.dumps(orden), json.dumps(response))
            return response, 500


# Configuración Flask
app = Flask(__name__)
cors = CORS(app)
app.config['PROPAGATE_EXCEPTIONS'] = True
#app.config["JWT_SECRET_KEY"] = "JwBGj2B4XFAKhYmn8Pgk0vH2w7UvgYfXAJ32e5rs8vI="
app.config["JWT_SECRET_KEY"] = "GrkIDwv8flT3tkC8pxRQOLcELnfyx4o2tN5lJXqQabvHMzcPSwGypsinRDma2UXz"
app_context = app.app_context()
app_context.push()
jwt = JWTManager(app)
api = Api(app)

# Agregamos el recurso que expone la funcionalidad ventas
api.add_resource(RegistrarOrdenResource, '/cpp/ventas')
api.add_resource(ActualizarOrdenResource, '/cpp/ventas/<int:orden_id>')

# Agregamos el recurso que expone la funcionalidad ventas
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
