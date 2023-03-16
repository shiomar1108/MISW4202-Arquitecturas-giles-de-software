import traceback
import pika
from cryptography.fernet import Fernet
from jproperties import Properties
from datetime import datetime


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
    estatus = 'SUCCESS'
    response = 'Orden registrada'
    print(str(method_frame))
    print(str(header_frame))
    with open('log_post_orders.txt', 'a') as file:
        registry_log('log_post_orders.txt', estatus,
                     body.decode(), response)
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
        traceback.print_exc()
        continue
    except pika.exceptions.AMQPChannelError as peache:
        traceback.print_exc()
        break
    except pika.exceptions.AMQPConnectionError as peace:
        traceback.print_exc()
        continue
