# CPP Experimento de Arquitectura 2

## Integrantes:

|   Nombre                         |   Correo                    |
|----------------------------------|-----------------------------|
| Jhon Fredy Guzmán Caicedo        | jf.guzmanc1@uniandes.edu.co |
| Haiber Humberto Galindo Sanchez  | h.galindos@uniandes.edu.co  |
| Oscar Uriel Tobar Rios           | o.tobar@uniandes.edu.co     |
| Shiomar Alberto Salazar Castillo | s.salazarc@uniandes.edu.co  |

## Propósito del experimento:
Este experimento tiene como propósito comprobar las siguientes tácticas  de arquitectura basados en la familia de resistir ataques y recuperacion de ataques mejoraremos la seguridad de nuestra aplicación.
* Reduccion de Superficie de Ataque: mediante el uso del ApiGateway Krakend se dara solo un punto de acceso a las APIs construidas.
* Autenticar Actores: Mediante el uso de Tokens de acceso controlados por un tercero con la plataforma de Atuh0 se permitira autenticarse en nuestras APIs para poderlas consumir.
* Autorizar Actores: Mediante el uso de perfiles se limitara el acceso a funcionalidades dentro de las APIS.
* Manejo de logs de eventos: los Microservicios y el apigateway contaran con logs paraidentificar las transacciones entrantes a nuestras APIS.



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

  
  ![image](https://user-images.githubusercontent.com/110913673/221440046-95944fa5-8c79-4daf-a112-64707d177d8e.png)



## Descripcion de los componentes que hacen parte del experimento:

### Microservicio de Ventas
El microservicio de Venta es el encargado de procesar las ordenes de ventas que realizan los vendedores a los clientes, de igual forma este microservicio debe recibir y encolar las solicitudes de edición de registros de ventas.
Se espera que este microservicio valide la información ingresada por los vendedores tales como ID del Cliente, dirección, Productos y cantidad de productos, y emita la información al Microservicio de Registro de Venta.
Así mismo se espera que este microservicio valide la existencia de un registro de venta antes de encolar las solicitudes de edición de orden de venta.

### Microservicio de Registro de la Venta
El microservicio de Registro de Venta es el encargado de guardar en la base de datos las ordenes procesadas y validadas por el microservicio de ventas, además debe ser capaz de procesar las ordenes de edición provenientes del microservicio de ventas.
Se espera que este microservicio tome los mensajes de la plataforma de mensajería y sea capaz guardar de forma correcta la información en la base de datos correspondiente.
De igual forma se espera que microservicio de Registro de Venta tome las solicitudes de edición de registros de venta y los aplique a los registros previamente creados.

### Microservicio ruta de clientes
El microservicio de Ruta Cliente es el encargado de regresar una lista de clientes que se deben visitar según el repartidor que ingrese al sistema.
Se espero que este microservicio muestre solo la información de los conductores autenticados y prevenga cualquier consulta que no provenga de un usuario conductores.

### ApiGateway KrakenD
El Apigateway es un componente dentro de la arquitectura estilo microservicios que tiene varias funciones, entre ellas las siguientes:
- Proveer un solo punto de acceso a las APIs y que estas no sean uasadas directamentes por los consumidores.
- Proveer mecanismos de filtrados de Ips, Autenticación  de las Apis expuestas.
- Balancear las cargas dentre las diferentes instancias de los microservicios creados.
- Generar metricas y registro de logs de todos los accesos de las aplicaciones.
en la siguiente imagen se muestra un conjunto de aplicaciones de terceros que se pueden usar en conjunto con KrakenD

![image](https://user-images.githubusercontent.com/65821560/226144810-2bf0d440-1e32-4e34-9c85-b7916b77cf8a.png)



### Proveed de Seguridad Auth0
Auth0 es una plataforma de gestión de identidades basada en la nube que está diseñada para ayudar a las empresas de diversos sectores, como finanzas, salud, medios de comunicación, comercio minorista y turismo, a gestionar de forma segura las actividades de autenticacion, autorizacion,  inicio de sesión, los perfiles de usuario y las credenciales.

En la siguiente imagen se ilustra el flujo de autenticación usando Auth0 y Krakend.
![image](https://user-images.githubusercontent.com/65821560/226144881-7211a277-c34f-4a87-a2b4-1008e5fb6816.png)


## Demostración ejecución pruebas

### Collection de Postman para ejecucion de pruebas
Sedebe descomprimir y luego importar en postman
[EXP_SEC_ARQ_CPP.postman_collection.json.zip](https://github.com/shiomar-salazar/MISW4202-11-Equipo1/files/11009833/EXP_SEC_ARQ_CPP.postman_collection.json.zip)

