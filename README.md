# CPP Experimento de Arquitectura 1

## Integrantes:

|   Nombre                         |   Correo                    |
|----------------------------------|-----------------------------|
| Jhon Fredy Guzmán Caicedo        | jf.guzmanc1@uniandes.edu.co |
| Haiber Humberto Galindo Sanchez  | h.galindos@uniandes.edu.co  |
| Oscar Uriel Tobar Rios           | o.tobar@uniandes.edu.co     |
| Shiomar Alberto Salazar Castillo | s.salazarc@uniandes.edu.co  |

## Propósito del experimento:
Este experimento tiene como propósito comprobar las siguientes tácticas de arquitectura
- Táctica de enmascaramiento manejo de fallas donde a través de un log se buscará registrar los errores presentados en la transacción que procesa la venta y redirigir la transacción a uno de los microservicios disponibles.
- Táctica de reconfiguración que permita identificar cuando un microservicio se encuentre fuera de línea y se redirija la petición a un microservicio disponible para atender la solicitud.
- Táctica de manejo de Errores donde al realizar validaciones de datos de entrada  se identificarán campos faltantes y se llenarán con valores por defecto para evitar que la transacción genere un resultado erróneo.


## Historias de arquitecturas seleccionadas
-	Como Vendedor cuando se genere una orden de venta dado a que la petición viene con Información Faltante, el sistema debe guardar un log de error y rellenar la información con valores por defecto, para poder procesar la petición de orden de venta de forma normal. Esto debe ocurrir el 95% de las veces.
-	Como Vendedor cuando al generar una orden de venta, dado que el sistema opera en Falla de Comunicación, el sistema debe Guardar un log de error y otro componente debe atender la petición, para que se pueda procesar la orden de forma correcta.  Esto debe suceder en menos de un minuto el 95% de las veces.


## Puntos de sensibilidad del experimento
-	Validar la capacidad del sistema para redireccionar peticiones en caso de fallas de uno de las instancias del Microservicio de Ventas.
-	Validar la capacidad del sistema para enmascarar información que viene incompleta o errónea.

## Instalación de componentes:

- En primera instancia se debe tener instalado **Docker**. Para esto se comparten los siguientes enlaces:
  - **Instalación de docker en Windows**: https://docs.docker.com/desktop/install/windows-install
  - **Instalación de docker en Linux Ubuntu**: https://docs.docker.com/engine/install/ubuntu
  - **Instalación de docker en Mac**: https://docs.docker.com/desktop/install/mac-install
- Para realizar las pruebas se debe instalar **JMeter**. 
  - Versión: `apache-jmeter-5.3`
  - Versión JAVA: `1.8.0_101`
  - Se comparte el siguiente enlace https://www.simplilearn.com/tutorials/jmeter-tutorial/jmeter-installation
- Se debe clonar el proyecto **MISW4202-11-Equipo1**: https://github.com/shiomar-salazar/MISW4202-11-Equipo1

## Ejecución:

- **Docker**:
  - Desde la raiz del proyecto, se debe ejecutar en una terminal el siguiente comando **`docker compose up`** para que docker a través del archivo **`docker-compose.yaml`** realice la creación de las imagenes y el despliegue de los contenedores.
  
  ![image](https://user-images.githubusercontent.com/110913673/221440046-95944fa5-8c79-4daf-a112-64707d177d8e.png)

- **JMeter**:

Ir a la carpeta **`bin`** donde se instalo JMeter y ejecutar el archivo **`jmeter.bat`**.

![image](https://user-images.githubusercontent.com/110913673/221445381-c93eefe5-b9c1-40eb-9d31-daf2de0bcacc.png)

Una vez abierto JMeter ir a **`File`** -> **`Open`**.

![image](https://user-images.githubusercontent.com/110913673/221445579-d0d7dd73-03d1-4ac6-908c-e716b8ea956d.png)

Seleccionamos el archivo **`Experimento.jmx`** que se encuentra en la ruta **`MISW4202-11-Equipo1/Jmeter`**.

![image](https://user-images.githubusercontent.com/110913673/221445834-259d2259-782b-4449-a956-eae8af41a048.png)

Por ultimo se ejecuta las pruebas.

![image](https://user-images.githubusercontent.com/110913673/221446161-bda2d2ba-2fe6-41cb-9c9e-6338cac4f3d5.png)


## Descripcion de los componentes que hacen parte del experimento:

### Microservicio de Ventas

Microservicio principal que tiene como objetivo:
- Validar y autocompletar la información recibida.
- Realizar el envió de la información ya completada a la cola de Redis.
- Se implementaran 3 contendores de este microservicio.


### Microservicio de Registro de Ventas
Microservicio secundario que tiene como objetivo:
- Realizar el desencolamiento de información almacenada en la cola de Redis.
- Registrar la información obtenida en un log.


### NGINX
Servidor web que tiene como objetivo:
-	Servir de API Gateway para centralizar las diferentes peticiones que llegan.
-	Servir de Balanceador para distribuir las peticiones entre los 3 contenedores con que tienen las instancias del Microservicio de Ventas


### Redis
Cola de mensajería utilizada persistir la información. Esta cola es utilizada por los Microservicios de Ventas y Registro de ventas de la siguiente manera:
-	Microservicio de Ventas: es el **publicador** y se encarga de enviar la información ya validada y autocompleta hacia la cola de Redis
-	Microservicio de Registro de Ventas: es el **suscriptor** y se encarga de desencolar la información de la cola de Redis.

## Demostración ejecución pruebas
Se comparte el siguiente enlace donde se evidencia la ejecución de los casos de prueba y el análisis de cada uno: https://youtu.be/yR7UWRQSTDc
