import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)

while True:
    for i in range(0, redis.llen('ventas')):
        #Procesar orden de Venta
        mensaje = redis.lpop('ventas')
        with open('log_registroVenta.txt','a') as file:
            file.write(f"{str(mensaje)}\n")