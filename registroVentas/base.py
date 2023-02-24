import redis

r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    decode_responses=True
)

cola = r.pubsub()

cola.subscribe('ventas')


for message in cola.listen():
    print(message['data'])