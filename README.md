# CPP Experimento de Arquitectura 2

## Integrantes:

|   Nombre                         |   Correo                    |
|----------------------------------|-----------------------------|
| Jhon Fredy Guzmán Caicedo        | jf.guzmanc1@uniandes.edu.co |
| Haiber Humberto Galindo Sanchez  | h.galindos@uniandes.edu.co  |
| Oscar Uriel Tobar Rios           | o.tobar@uniandes.edu.co     |
| Shiomar Alberto Salazar Castillo | s.salazarc@uniandes.edu.co  |

## Propósito del experimento:
Este experimento tiene como propósito comprobar las siguientes tácticas de arquitectura basados en la familia de resistir ataques y recuperación de ataques mejoraremos la seguridad de nuestra aplicación.
* **Reducción de Superficie de Ataque:** Se definirá un único punto de acceso al sistema a través del uso de un API Gateway. 
* **Autenticar Actores y Control de acceso basada en tokens de seguridad:** Mediante el uso de Tokens de acceso controlados por un tercero con la plataforma de Atuh0 se permitirá autenticarse en nuestras APIs para poderlas consumir.
* **Autorizar Actores:** Mediante el uso de perfiles se limitará el acceso a funcionalidades dentro de las APIS.
* **Manejo de logs de eventos:** Los Microservicios y el Api Gateway contarán con logs propios, que permitirán dejar un registro del estado del sistema en todo momento.
* **Separación de entidades:** A través de Docker se contenerizaran los diferentes componentes que hacen parte del experimento, proporcionando entornos independientes de ejecución.
* **Limitación de acceso a los recursos:** Al estar contenerizados todos los componentes que hacen parte del experimento, la única forma de poder llegar a ellos es a través del Api Gateway, si se tratase de consumir un recurso de forma directa no se podría.


## Historias de arquitecturas seleccionadas
* Como empleado de Marketing y Ventas cuando genere una orden de venta dado que el sistema opera normalmente quiero ser el único que pueda realizar alguna modificación en dicha orden para garantizar que quien genero la orden inicial es quien puede modificarla y no alguien más. Esto debe suceder 100% de las veces.
* Como Transportista cuando existan ingresos al sistema dado que el sistema opera normalmente quiero que se garantice que el ingreso al sistema haya sido autorizado por mi mismo para garantizar que si sea yo el que hace los movimientos en la plataforma. Esto debe suceder el 100% de las veces.


## Puntos de sensibilidad del experimento
* Garantizar que al 100 % de las peticiones realizadas sea validado el acceso y rol  del consumidor  y que solo pueda realizar acciones permitidas acorde a su rol
* Garantizar que al 100 % de las peticiones realizadas sea validado el acceso desde terminales autorizadas al microservicio y registrar en logs todas las transacciones realizadas

## Instalación de componentes:
- En primera instancia se debe tener instalado **Docker**. Para esto se comparten los siguientes enlaces:
  - **Instalación de docker en Windows**: https://docs.docker.com/desktop/install/windows-install
  - **Instalación de docker en Linux Ubuntu**: https://docs.docker.com/engine/install/ubuntu
  - **Instalación de docker en Mac**: https://docs.docker.
  - Se debe clonar el proyecto **MISW4202-11-Equipo1**: https://github.com/shiomar-salazar/MISW4202-11-Equipo1
  
- **Docker**:
  - Desde la raiz del proyecto, se debe ejecutar en una terminal el siguiente comando **`docker compose up`** para que docker a través del archivo **`docker-compose.yaml`** realice la creación de las imagenes y el despliegue de los contenedores.

  ![image](https://user-images.githubusercontent.com/110913673/226149293-ff6db13e-135c-4b0a-bdf8-c43fba304a39.png)

## Descripcion de los componentes que hacen parte del experimento:

### Microservicio de Ventas
El microservicio de Venta es el encargado de procesar las ordenes de ventas que realizan los vendedores a los clientes, de igual forma este microservicio debe recibir y encolar las solicitudes de edición de órdenes de ventas previamente creadas.
Se espera que este microservicio reciba las órdenes de venta ingresadas por los vendedores y posteriormente haga el envió a la cola RabbitMQ correspondiente (cola de creación o cola de actualización) siempre y cuando las credenciales sean correctas.
Así mismo se espera que este microservicio registre logs en cada transacción que se realice ya sea un flujo exitoso o de error.
Las propiedades de conectividad a la colas `post_orders_queue` y `put_orders_queue` se encuentran en el archivo de propiedades `app-config.properties`.


### Microservicio de Registro de orden de Venta POST
El microservicio de Registro de Venta es el encargado de estar escuchando la cola RabbitMQ de creación de órdenes y una vez detecte un nuevo mensaje, desencole y registra la información obtenido en el log `log_post_orders.txt`.
Las propiedades de conectividad a la cola `post_orders_queue` se encuentran en el archivo de propiedades `app-config.properties`.

### Microservicio de Registro de orden de Venta PUT
El microservicio de Registro de Venta es el encargado de estar escuchando la cola RabbitMQ de actualización de órdenes y una vez detecte un nuevo mensaje, desencola el mensaje, valida si el ID de la orden existe y posteriormente registra en el log `log_put_orders.txt` el resultado, si fue exitoso (se actualiza al orden) o si se presentó un error (orden inexistente).
Las propiedades de conectividad a la cola `put_orders_queue` se encuentran en el archivo de propiedades `app-config.properties`.

![image](https://user-images.githubusercontent.com/110913673/226152083-6bc436f4-65d2-4ce2-a554-0333f38d1ff0.png)

### Microservicio ruta de clientes
El microservicio de Ruta Cliente es el encargado de regresar una lista de clientes que se deben visitar según el repartidor que ingrese al sistema.
Se espero que este microservicio muestre solo la información de los conductores autenticados y prevenga cualquier consulta que no provenga de un usuario conductores.

![image](https://user-images.githubusercontent.com/110913673/226152015-da55c2a0-312b-4d31-8612-60e42349fe1c.png)

### ApiGateway KrakenD
El Api Gateway es un componente dentro de la arquitectura estilo microservicios que tiene varias funciones, entre ellas las siguientes:
- Proveer un solo punto de acceso a las APIs y que estas no sean usadas directamente por los consumidores.
- Proveer mecanismos de filtrados de IPs, Autenticación de las Apis expuestas.
- Balancear las cargas entre las diferentes instancias de los microservicios creados.
- Generar métricas y registro de logs de todos los accesos de las aplicaciones.
en la siguiente imagen se muestra un conjunto de aplicaciones de terceros que se pueden usar en conjunto con KrakenD

![image](https://user-images.githubusercontent.com/65821560/226144810-2bf0d440-1e32-4e34-9c85-b7916b77cf8a.png)

### Proveedor de Seguridad Auth0
Auth0 es una plataforma de gestión de identidades basada en la nube que está diseñada para ayudar a las empresas de diversos sectores, como finanzas, salud, medios de comunicación, comercio minorista y turismo, a gestionar de forma segura las actividades de autenticación, autorización, inicio de sesión, los perfiles de usuario y las credenciales.

En la siguiente imagen se ilustra el flujo de autenticación usando Auth0 y Krakend.
![image](https://user-images.githubusercontent.com/65821560/226144881-7211a277-c34f-4a87-a2b4-1008e5fb6816.png)


## Demostración ejecución pruebas



### Collection de Postman para ejecución de pruebas
Se debe descomprimir y luego importar en la herramienta Postman
[EXP_SEC_ARQ_CPP.postman_collection.json.zip](https://github.com/shiomar-salazar/MISW4202-11-Equipo1/files/11009833/EXP_SEC_ARQ_CPP.postman_collection.json.zip)

