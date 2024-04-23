import os
from threading import Thread
import telebot
import logging, logging.config
from geopy.geocoders import Nominatim
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

from weather import Weather

from dotenv import load_dotenv

class TelegramWeatherBot():
    def __init__(self):
        self.BOT_TOKEN = '6801086874:AAHeCvum2Rsh0API-nEK41vzuO7zCRR3_KY'
        self.WEATHER_TOKEN = '03073a99421b1d8b922aa51d4b1b9be8'
        self.POLLING_TIMEOUT = None
        self.bot = telebot.TeleBot(self.BOT_TOKEN)
        self.weather = Weather(self.WEATHER_TOKEN)
        self.command_handler()

        self.subscribed_dict = {}

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

        self.scheduler = BlockingScheduler()
        #self.scheduler.add_job(self.send_automatic_weather,"cron",hour=10,min=40)
        self.scheduler.add_job(self.send_automatic_weather,"interval",minutes=1)
        Thread(target=self.schedule_checker).start()

        print('Starting...')

        print("Starting polling...")
        self.bot.infinity_polling()

    def schedule_checker(self):
        while True:
            self.scheduler.start()

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
        
        @self.bot.message_handler(commands=['auto'])
        def auto_weather(message):
            self.bot.send_message(message.chat.id, 'Te estas subscribiendo al sistema automatico')
            sent_message = self.bot.send_message(message.chat.id, '¿Qué ciudad te interesa?')
            self.bot.register_next_step_handler(sent_message, callback=self.subscribe_weather)
        
        @self.bot.message_handler(func=lambda msg: True)
        def echo_all(message):
            self.bot.send_message(message.chat.id, 'No entendi :(')

    def send_weather(self,message):
        weather_message = self.weather.fetch_weather(message.text)
        self.bot.send_message(message.chat.id, 'Ahí está el clima!')
        self.bot.send_message(message.chat.id, weather_message, parse_mode='Markdown')
        url = 'https://openweathermap.org/img/wn/{}@2x.png'.format('10n')
        self.bot.send_photo(message.chat.id, photo= url)

    def send_automatic_weather(self):
        for chat_id,location in self.subscribed_dict.items():
            weather_message = self.weather.fetch_weather(location)
            self.bot.send_message(chat_id, 'Ahí está el clima!')
            self.bot.send_message(chat_id, weather_message, parse_mode='Markdown')
            url = 'https://openweathermap.org/img/wn/{}@2x.png'.format('10n')
            self.bot.send_photo(chat_id, photo= url)

    def subscribe_weather(self,message):
        self.subscribed_dict[message.chat.id] = message.text
        self.bot.send_message(message.chat.id, 'Te subscribiste al sistema automatico!')



    def echo_all(self,message):
        '''
        echoes back any other messages bot receives from user
        '''
        self.bot.reply_to(message, message.text)

#weatherbot = TelegramWeatherBot()