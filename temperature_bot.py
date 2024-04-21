import os
import telebot
import requests
import logging, logging.config
from dotenv import load_dotenv
from geopy.geocoders import Nominatim

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEATHER_TOKEN = os.environ.get('WEATHER_TOKEN')
POLLING_TIMEOUT = None
bot = telebot.TeleBot(BOT_TOKEN)
print('Starting...')


config = {
    'disable_existing_loggers': False,
    'version': 1,
    'formatters': {
        'short': {
            'format': '%(asctime)s %(levelname)s %(message)s',
        },
        'long': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'short',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'plugins': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        }
    },
}
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)

@bot.message_handler(commands=['hola'])
def send_welcome(message):
    
    bot.send_message(message.chat.id, 'Hola!!')


@bot.message_handler(commands=['clima'])
def send_weather(message):
    location = '¿Qué ciudad te interesa? '
    sent_message = bot.send_message(message.chat.id, location, parse_mode='Markdown')
    bot.register_next_step_handler(sent_message, fetch_weather)
    return location


def location_handler(message):
    '''
    returns the latitude and longitude coordinated from user's message (location) using the Nominatim geocoder.
    if location is found - returns the rounded latitude and longitude
    else - returns Location not found
    '''
    location = message.text
    # Create a geocoder instance
    geolocator = Nominatim(user_agent="my_app")

    try:
        # Get the latitude and longitude
        location_data = geolocator.geocode(location)
        latitude = round(location_data.latitude,2)
        longitude = round(location_data.longitude,2)
        logger.info("Latitude '%s' and Longitude '%s' found for location '%s'", latitude, longitude, location)
        return latitude, longitude
    except AttributeError:
        logger.exception('Location not found', exc_info=True)


def get_weather(latitude,longitude):
    '''
    arguments - latitude, longitude
    takes in arguments as inputs and constructs URL to make API call to OpenWeatherMap API
    returns a response JSON after fetching weather data for the specified latitude and longitude
    '''
    url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&units={}&lang={}&appid={}'.format(latitude, longitude, 'metric', 'es', WEATHER_TOKEN)
    response = requests.get(url)
    #print(response.json())
    return response.json()

    
def fetch_weather(message): 
    '''
    called when the user provides location in response to the '/weather' command.
    uses the 'location_handler' function to get latitude & longitude of the provided location and 'get_weather' function to fetch the weather data
    extracts weather description from API response and sends to user as message.
    '''
    latitude, longitude = location_handler(message)
    weather = get_weather(latitude,longitude)
    data = weather['list']
    data_2 = data[3]
    info_weather = data_2['weather']
    info_main= data_2['main']
    temp= info_main['temp']
    temp_max= info_main['temp_max']
    temp_min= info_main['temp_min']
    feels_like=info_main['feels_like']
    data_3 = info_weather[0]
    description = data_3['description']
    icon = data_3['icon']
    weather_message = f'*Temperatura de hoy será:* {temp}°C\n *Sensación térmica:* {feels_like}°C\n *Temperatura máxima:* {temp_max}°C\n *Temperatura mínima:* {temp_min}°C\n *Descripción:* {description}\n'
    bot.send_message(message.chat.id, 'Ahí está el clima!')
    bot.send_message(message.chat.id, weather_message, parse_mode='Markdown')
    url = 'https://openweathermap.org/img/wn/{}@2x.png' .format(icon)
    bot.send_photo(message.chat.id, photo= url)


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    '''
    echoes back any other messages bot receives from user
    '''
    bot.reply_to(message, message.text)

bot.infinity_polling()