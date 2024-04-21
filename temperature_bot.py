import os
import telebot
import logging, logging.config
from geopy.geocoders import Nominatim
import requests

from weather import Weather

from dotenv import load_dotenv

class TelegramWeatherBot():
    def __init__(self):
        self.BOT_TOKEN = '7007180975:AAFK3P7eOyonHF5pSj_vStvWrGluN3Fohb8'
        self.WEATHER_TOKEN = '03073a99421b1d8b922aa51d4b1b9be8'
        self.POLLING_TIMEOUT = None
        self.bot = telebot.TeleBot(self.BOT_TOKEN)
        self.weather = Weather(self.WEATHER_TOKEN)
        self.command_handler()


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
        self.logger = logging.getLogger(__name__)

        print('Starting...')

        print("Starting polling...")
        self.bot.infinity_polling()

    def command_handler(self):
        @self.bot.message_handler(commands=['hola'])
        def send_welcome(message):
            self.bot.send_message(message.chat.id, 'Hola!!')

        @self.bot.message_handler(commands=['clima'])
        def send_weather(message):
            location = '¿Qué ciudad te interesa? '
            sent_message = self.bot.send_message(message.chat.id, location, parse_mode='Markdown')
            self.bot.register_next_step_handler(sent_message, callback=self.send_weather)
            return location
        
        @self.bot.message_handler(func=lambda msg: True)
        def echo_all(message):
            '''
            echoes back any other messages bot receives from user
            '''
            self.bot.reply_to(message, message.text)

    def send_weather(self,message):
        weather_message = self.weather.fetch_weather(message)
        self.bot.send_message(message.chat.id, 'Ahí está el clima!')
        self.bot.send_message(message.chat.id, weather_message, parse_mode='Markdown')
        url = 'https://openweathermap.org/img/wn/{}@2x.png'.format('10n')
        self.bot.send_photo(message.chat.id, photo= url)

    def echo_all(self,message):
        '''
        echoes back any other messages bot receives from user
        '''
        self.bot.reply_to(message, message.text)

#weatherbot = TelegramWeatherBot()