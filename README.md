# APLICACION_KEEPCODING: My Daily Stock Market
###### Por Sara Díaz - Proyecto Bootcamp Cero KeepCoding


###


Debemos tener descargado git y python3 en nuestro ordenador.
Git: https://git-scm.com/downloads
Python3: https://www.python.org/downloads/
Una vez hecho esto, abrimos nuestro terminal, entramos en la carpeta donde vamos a alojar el proyecto y escribimos:
git clone https://github.com/sdiamar/APLICACION_KEEPCODING.git
Ahora entramos en la carpeta especificada:
cd APLICACION_KEEPCODING

Una vez dentro, desplegamos un entorno virtual: 
python -m venv env
Y lo activamos:
WINDOWS: env\Scripts\activate.bat
MAC: source ./env/bin/activate

Nos fijaremos que estamos dentro del entorno porque aparece (env) en la línea de comandos.

Podemos lanzar la aplicación a Visual Studio Code así: code .
O podemos seguir en el terminal. En cualquier caso, lo primero que hay que hacer es instalar las dependencias del archivo requirements.
Para ello, escribirmos en el terminal dentro del entorno (ya sea en Visual Studio Code o en el terminal del sistema): pip install -r requirements.txt
Esto instalará todos los paquetes necesarios para que la aplicación funcione.

No tenemos que decirle al sistema cuál es nuestra aplicación y cuál nuestro entorno de Flask porque el paquete python-dotenv lee nuestro archivo .env, donde hemos dejado las instrucciones para que lo rellenes. Así que ahora hay que hacer un nuevo archivo .env donde daremos las instrucciones que hemos aportado en el archivo env_template. Se puede hacer con un bloc de notas.
En concreto, los parámetros que debes indicar son:
Para configurar el servidor de correo, deberás hacerlo con tu proveedor. En caso de tener problemas, he generado una dirección de prueba para poder probar el servicio de email, ya que si no, no se podrá acceder a la aplicación:
admin_email = prueba@inversia500.com
password_email = niknyz-wudNeq-viwwe0
server_email = mail.inversia500.com
Este email de dará de baja a finales de mes.
Una vez que tenemos el archivo terminado, corremos en nuestro terminal la aplicación con: flask run

Ello ejecuta nuestra apliación en la dirección local: http://127.0.0.1:5000/
Felicidades, ya puedes gestionar My Daily Stock Market.
