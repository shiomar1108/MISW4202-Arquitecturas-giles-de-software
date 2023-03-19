import json
import pika
from cryptography.fernet import Fernet
from jproperties import Properties
from datetime import datetime


# Function to read json data
def load_data():
    file = open('app-data.json')
    return json.load(file)


# Function to validate data
def get_response(data, orden_id):
    print(data)
    for orden in data:
        if str(orden['id']) == str(orden_id):
            return ['SUCCESS', f'Orden [{orden_id}] actualizada']
    return ['WARNING', f'La orden [{orden_id}] no se encuentra registrada en el sistema']


# Function to registry log
def registry_log(file, severity, request, response):
    with open(file, 'a') as file:
        file.write(
            f"[{severity}]-[{datetime.now()}]-[request=>{request}]-[response=>{response}]\n")


# Function to read key
def load_security_key(key):
    return open(key, "rb").read()


# Function to decrypt key
def decrypt(key_to_decrypt):
    security_key = load_security_key('security.key')
    decrypt = Fernet(security_key)
    decryptedValue = decrypt.decrypt(key_to_decrypt)
    return decryptedValue


# Function to read properti decrypted
def read_property(properti):
    configs = Properties()
    with open('app-config.properties', 'rb') as config_file:
        configs.load(config_file)
    return decrypt(configs[properti].data)


# Function to listen messages in queue
def on_message(channel, method_frame, header_frame, body):
    json_data = json.loads(body.decode())
    print(str(method_frame))
    print(str(header_frame))
    response = get_response(load_data(), json_data['id'])
    registry_log('log_put_orders.txt', response[0],
                 json.dumps(json_data), response[1])
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


# Listener
while (True):
    try:
        rabbit_host = read_property('HOST_RABBIT').decode()
        virtual_host = read_property('VIRTUAL_HOST').decode()
        rabbit_user = read_property('USER_QUEUE').decode()
        rabbit_password = read_property('PASSWORD_QUEUE').decode()
        queue = read_property('QUEUE').decode()
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host, virtual_host=virtual_host,
                                                                       credentials=pika.PlainCredentials(rabbit_user, rabbit_password)))
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)
        channel.queue_declare(queue, durable=True)
        channel.basic_consume(queue, on_message)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
            connection.close()
            break
    except pika.exceptions.ConnectionClosedByBroker as peccbb:
        print(str(peccbb))
        continue
    except pika.exceptions.AMQPChannelError as peache:
        print(str(peache))
        break
    except pika.exceptions.AMQPConnectionError as peace:
        print(str(peace))
        continue
