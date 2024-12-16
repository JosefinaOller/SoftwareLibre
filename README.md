🌦️ Clima Bot - Telegram Chatbot

¡Bienvenido a Clima Bot!
Este proyecto fue desarrollado por Joel Coyos y Josefina Oller como parte del trabajo práctico de Software Libre en la Universidad Nacional de Mar del Plata.

Clima Bot es un chatbot de Telegram que permite consultar el clima actual en cualquier ciudad y configurar notificaciones automáticas del clima a intervalos regulares. Es una herramienta práctica para quienes necesitan información meteorológica de forma rápida y accesible.

🚀 Funcionalidades

Consultar el clima actual: Ingresa el nombre de una ciudad y obtén el clima actualizado al instante. 
Clima automático: Recibe el reporte del clima de tu ciudad u otra elegida a intervalos regulares. Comandos útiles: 
/hola: Saluda al bot.
/clima: Solicita el clima actual de una ciudad.
/auto: Activa las notificaciones automáticas del clima. 

🛠️ Instalación y Configuración

1. Instalar dependencias necesarias:

Ejecuta los siguientes comandos para instalar las dependencias requeridas:

pip install requests pyTelegramBotAPI geopy python-dotenv 

2. Activar el daemon del bot:

Para iniciar el bot, utiliza:

python weatherdaemon.py start 

Para detener el bot, utiliza:

python weatherdaemon.py stop 

3. Buscar el bot en Telegram:

Abre Telegram y busca: @UNMDPBot. Inicia el chat con el bot. 

📝 Uso

Escribe alguno de los siguientes comandos en el chat:

/hola: Saluda y verifica que el bot esté funcionando correctamente. 
/clima: Solicita el clima actual. El bot te pedirá el nombre de la ciudad (sin barras ni símbolos adicionales). 
/auto: Configura el envío automático del clima para una ciudad a intervalos de tiempo. 

Responde las preguntas del bot de manera natural, indicando el nombre de la ciudad de interés.

🌐 Requisitos

Python 3.7+ 
Cuenta activa en Telegram. 

🔧 Dependencias Utilizadas

Requests: Para realizar solicitudes a la API de clima. 
pyTelegramBotAPI: Para integrar el bot con Telegram. 
Geopy: Para procesar ubicaciones y obtener coordenadas. 
python-dotenv: Para manejar configuraciones sensibles (como claves de API). 

💡 Notas Adicionales

Recuerda tener tu archivo .env configurado con las claves necesarias, como el token de tu bot de Telegram y la clave de la API de clima. Si el daemon no responde correctamente, verifica los permisos y configuraciones del sistema.
