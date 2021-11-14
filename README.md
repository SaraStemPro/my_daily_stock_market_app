# MY DAILY STOCK MARKET
###### Por Sara Díaz - Proyecto Bootcamp Cero KeepCoding

> _De pequeños comienzos, surgen grandes cosas._ - Anónimo

## Instalación previa

Para iniciar este proyecto, debemos tener descargado "Git" y "Python3" en nuestro ordenador. Los podemos encontrar en:
- __Git__: https://git-scm.com/downloads
- __Python3__: https://www.python.org/downloads/

## Terminal

Una vez descargados, abrimos nuestro terminal, y seguimos los siguientes pasos:

1. Entramos en la carpeta donde vamos a alojar el proyecto y escribimos el siguiente código: 

`git clone https://github.com/sdiamar/my_daily_stock_market_app_keepcoding.git`

2. Entramos en la carpeta especificada:

`cd my_daily_stock_market_app_keepcoding`

3. Una vez dentro, desplegamos un entorno virtual del siguiente modo: 

`python -m venv env`

Si no funciona, probamos con:

`python3 -m venv env`

4. Activamos el entorno virtual "env":

En Windows: 

`env\Scripts\activate.bat`

En Mac: 

`source ./env/bin/activate`

Nos fijaremos que estamos dentro del entorno porque aparece __(env)__ en la línea de comandos.

5. Podemos lanzar la aplicación a Visual Studio Code del siguiente modo (aunque también podemos continuar en el terminal): 

`code .` 

## Instalación de dependencias para el proyecto

Completados los pasos anteriores, debemos instalar las dependencias para que la aplicación funcione correctamente.
Esto lo hacemos con la ayuda del archivo __"requirements.txt"__.

Para su instalación, escribimos en el terminal dentro del entorno (ya sea en Visual Studio Code o en el terminal del sistema): 

`pip install -r requirements.txt`

## Archivo .env con los parámetros a rellenar previamente

Este archivo es fundamental para la correcta ejecución de nuestra aplicación, ya que tendrá todos los datos iniciales necesarios. Hemos dejado un archivo llamado __"env_template"__ con un ejemplo de lo que debemos escribir en él. El archivo .env se puede generar como un archivo del bloc de notas donde podamos escribir lo necesario. En concreto, son los siguientes parámetros:

#### 1. Mailing

- __ADMIN_EMAIL__: Aquí debemos poner nuestro email, desde donde queremos que se envíe la clave de acceso al usuario.
- __ADMIN_PASSWORD__: Aquí debemos escribir la contraseña de nuestro email para que la librería pueda acceder al servicio de mailing.
- __SERVER_EMAIL__: Aquí debemos indicar el servidor de nuestro email.

Si no sabes o no puedes configurar el servidor de correo, hemos generado un email y password de prueba para que puedas comprobar el funcionamiento de la app. Éstos son:
- __ADMIN_EMAIL__=prueba@inversia500.com
- __ADMIN_PASSWORD__=niknyz-wudNeq-viwwe0
- __SERVER_EMAIL__=mail.inversia500.com

Este email se dará de baja a finales del _mes de noviembre 2021_.

#### 2. API KEY Alpha Vantage
Para conectar la app a datos históricos de acciones, hemos generado una API KEY totalmente gratuita con el proveedor de datos __Alpha Vantage__. Esta API puedes solicitarla en el siguiente enlace:
https://www.alphavantage.co/support/#support

- __API_ALPHA__: Ponemos aquí la API KEY generada en Alpha Vantage

#### 3. Parámentros de FLASK

Flask es un framework que hará que nuestra aplicación funcione. Flask necesita conocer cuál es el __nombre de nuestra aplicación y nuestro entorno de trabajo__. En nuestro caso, se lo decimos al sistema a través del arhivo .env. Esto se puede hacer así gracias a que hemos descargado (anteriormente en requirements) el paquete _"python-dotenv"_ que lee nuestro archivo .env directamente con lo que necesita para ejecutar la aplicación.
Por tanto, en el archivo .env escribiremos:

- __FLASK_APP__: Aquí ponemos el nombre de la aplicación (en este caso "run")
- __FLASK_ENV__: Aquí podemos poner el entorno de desarrollo o producción (development | production)

## Ejecución de la aplicación con FLASK

Ahora sí lo tenemos todo preparado para poder ejecutar nuestra aplicación. 
Para ello, escribimos en nuestro terminal: 

`flask run`

Este comando ejecuta nuestra aplicación en la dirección local: 
http://127.0.0.1:5000/

Ingresando dentro de dicho enlace, podrás interactuar con la app.

__¡Felicidades! Ya puedes gestionar la app My Daily Stock Market.__

## Funcionamiento de la aplicación

Una vez dentro, el funcionamiento de la app será el siguiente:

1. La url anterior nos llevará a la página: __"Inicio de sesión"__, donde debemos introducir nuestro email (en estos momentos, solo hay dos usuarios registrados en la base de datos, mi profesor Tony y yo :)).
2. Una vez comprobado que el email está registrado, se le envía al usuario una __clave de acceso__ a su email (de ahí la configuración del servidor de mailing que hicimos antes). Esta clave será la que tenga que introducir para poder acceder al sistema. Veremos que si no inroducimos clave o la introducimos incorrectamente, nos llevará de vuelta a la página de inicio de sesión para que volvamos a escribir nuestro email y repetir el proceso 1 y 2 hasta que la clave sea la correcta, es decir, que sea la que se llega por email.
***NOTA IMPORTANTE***: Comprueba el correo no deseado si no recibes la clave en tu bandeja de entrada.
3. Una vez comprobado que el usuario, por tanto, está registrado y que la clave es correcta, entramos, por defecto, en la página __"Lista de acciones"__. Aquí disponemos de la lista de acciones que cada día muestra mi algoritmo de inversión. Este algoritmo no se aporta en esta práctica, y se basa en seguir valores de Bolsa que estén rompiendo la zona de resistencia para empezar una posible tendencia alcista.
4. La __navegación__ por la web es sencilla. A partir de este punto podemos interactuar con la aplicación como queramos, en concreto:
#### Página: Lista de acciones:
Los botones son:
- Podemos __marcar los valores de la lista como favoritos__ si queremos hacer un seguimiento de los mismos. Hay que recordar, que esta app es multiusuario y se compartirá con todos los usuarios registrados en la comunidad.
- Podemos ver la tabla de __datos históricos__ de los valores (gracias a la API de Alpha Vantage), si disponemos de sus datos. Además, podremos ver también el __gráfico__ con la tendencia del valor en el último año.

#### Página: Favoritos
Aquí se nos muestra la lista de favoritos actual. Los botones son:
- También podemos ver la tabla de __datos históricos__ de los valores, si disponemos de sus datos y ver el __gráfico__ con la tendencia del valor en el último año.
- Podemos consultar la __rentabilidad__ que llevaría el valor si se hubiese comprado en la fecha en la que se añadió a la lista de favoritos. He dejado algunos favoritos antiguos marcados para poder hacer este seguimiento.
- Por último, en esta página podemos __eliminar__ cualquier valor si no queremos hacerle el seguimiento (esto nos llevará a otra página de confirmación puesto que dicha acción repercutirá al resto de usuarios de la comunidad, ya que desaparecerá para todos).

#### Página: Salir
Para salir de la aplicación, dolo debemos pinchar ahí. Esto nos __cerrará la sesión__ automáticamente, y nos reenviará a la página de "Inicio de sesión", teniendo que volver a empezar si queremos interactuar de nuevo con la app.

---
__Con esto finaliza este Readme.__

---
## Agradecimientos
No es algo común escribir esto aquí, pero como es el único documento que entregamos, no me gustaría terminar sin agradecer a los profesores de KeepCoding, Tony y Ramón, que me han ayudado a la realización de este proyecto, sobre todo Tony. Han sido muchas horas dedicadas y el apoyo de este gran profesorado ha sido clave, con unos conocimientos extraordinarios.

Agradecer también a mi familia, mi marido y el bebé que está creciendo dentro de mi, porque me lo han puesto muy fácil y me han apoyado en todo. Sin duda el amor es lo más bonito que nos llevamos.

Ahora el siguiente paso es avanzar en la seguridad de la app para poder lanzarla al público dentro de mi blog. Así que sigue quedando trabajo por delante con mucha motivación.

__Espero que os guste, ¡gracias!__

__Sara Díaz__
